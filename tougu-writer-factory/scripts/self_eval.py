#!/usr/bin/env python3
"""
投顾写作Skill工厂 - 自测评辅助脚本

【定位说明】
本脚本是自测评的**辅助工具**，而非主评估器。
主评估流程在 `references/self_eval.md` 中由LLM驱动执行。

本脚本负责：
1. 特征提取：从样本和生成文章中提取7维度特征
2. 结构对比：计算各维度的匹配度得分
3. 格式校验：内置skill-creator规范校验（可调用外部skill-creator）

用法：
# 完整流程（Python辅助 + LLM判断）
python self_eval.py --skill-path <Skill路径> --reference-samples <案例路径> \
    --test-topic "今日收评" --generated-article <文章内容或文件> --output <报告路径>

# 仅格式校验（调用skill-creator或内置校验）
python self_eval.py --skill-path <Skill路径> --validate-format-only

# 仅风格对比（Python特征提取）
python self_eval.py --skill-path <Skill路径> --reference-samples <案例路径> --compare-style-only
"""

import argparse
import json
import os
import re
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Callable

# ============ 配置 ============

DIMENSION_WEIGHTS = {
    "标题格式": 0.20,
    "段落结构": 0.20,
    "分析逻辑": 0.20,
    "句式特征": 0.15,
    "特色词汇": 0.15,
    "固定表达": 0.10,
}

ACCEPTANCE_THRESHOLD = 0.80  # 整体≥80%通过
MIN_DIMENSION_SCORE = 0.50   # 任何维度<50%必须修复
MAX_ITERATIONS = 3


# ============ Skill Creator 格式校验（内置） ============
# 本模块对标 skill-creator 的格式规范
# 在 skill-creator 可用时优先调用外部校验，本模块作为内置后备

def validate_meta_skill(skill_path: str) -> Tuple[bool, List[str]]:
    """
    校验元skill（tougu-writer-factory）自身格式。
    只检查元skill应该拥有的文件，不检查生成物占位符文件。

    返回：(是否通过, 问题列表)
    """
    issues = []
    skill_md = Path(skill_path) / "SKILL.md"

    if not skill_md.exists():
        return False, ["[FAIL] SKILL.md not found in meta-skill"]

    content = skill_md.read_text(encoding="utf-8")

    # 1. YAML frontmatter 检查
    if not content.startswith("---"):
        issues.append("[FAIL] SKILL.md missing YAML frontmatter")
    else:
        parts = content.split("---", 2)
        if len(parts) < 3:
            issues.append("[FAIL] YAML frontmatter not properly closed")
        else:
            fm_text = parts[1]
            required_fields = ["name", "description"]
            for field in required_fields:
                if field not in fm_text:
                    issues.append(f"[FAIL] frontmatter missing required field: {field}")

    # 2. name 字段规范检查（元skill用-factory后缀）
    name_match = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
    if name_match:
        name_value = name_match.group(1).strip()
        if not re.match(r"^[a-z0-9_-]+$", name_value):
            issues.append(f"[FAIL] name field invalid: '{name_value}'")
        if not name_value.endswith("-factory"):
            issues.append(f"[WARN] name should end with '-factory' for meta-skill")

    # 3. description 字段检查
    desc_match = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)
    if desc_match:
        desc_value = desc_match.group(1).strip()
        if len(desc_value) > 200:
            issues.append(f"[WARN] description too long ({len(desc_value)} chars)")
    else:
        issues.append("[FAIL] frontmatter missing description")

    # 4. 章节结构检查
    required_sections = [
        ("任务目标", "任务目标|##.*任务"),
        ("操作步骤", "操作步骤|##.*操作"),
        ("注意事项", "注意事项|##.*注意"),
    ]
    for section_name, pattern in required_sections:
        if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            issues.append(f"[FAIL] SKILL.md missing required section: {section_name}")

    # 5. 元skill自身文件结构检查
    required_meta_files = [
        ("SKILL.md", skill_md),
        ("references/", Path(skill_path) / "references"),
        ("scripts/", Path(skill_path) / "scripts"),
        ("固化模块/", Path(skill_path) / "固化模块"),
        ("assets/", Path(skill_path) / "assets"),
    ]
    for name, path in required_meta_files:
        if name.endswith("/"):
            if not path.exists() or not path.is_dir():
                issues.append(f"[FAIL] Missing required directory: {name}")
        else:
            if not path.exists():
                issues.append(f"[FAIL] Missing required file: {name}")

    # 6. references 目录内容检查（元skill自身文件）
    refs_dir = Path(skill_path) / "references"
    if refs_dir.exists():
        required_refs = [
            "step1.md",
            "step2.md",
            "step3.md",
            "step4.md",
            "self_eval.md",
        ]
        for ref in required_refs:
            ref_path = refs_dir / ref
            if not ref_path.exists():
                issues.append(f"[FAIL] references/ missing file: {ref}")
            elif ref_path.stat().st_size < 50:
                issues.append(f"[WARN] references/{ref} too small, may be incomplete")

    # 7. scripts 目录内容检查（元skill自身文件）
    scripts_dir = Path(skill_path) / "scripts"
    if scripts_dir.exists():
        if not (scripts_dir / "self_eval.py").exists():
            issues.append("[FAIL] scripts/ missing self_eval.py")
        if not (scripts_dir / "market_data.md").exists():
            issues.append("[WARN] scripts/ missing market_data.md (LLM guide)")

    # 8. 固化模块目录检查
    guding_dir = Path(skill_path) / "固化模块"
    if guding_dir.exists():
        if not (guding_dir / "compliance.md").exists():
            issues.append("[WARN] 固化模块/ missing compliance.md")
        if not (guding_dir / "market_data.py").exists():
            issues.append("[WARN] 固化模块/ missing market_data.py")

    passed = len([i for i in issues if i.startswith("[FAIL]")]) == 0
    return passed, issues


def validate_generated_skill(skill_path: str) -> Tuple[bool, List[str]]:
    """
    校验生成的（具体）Skill是否符合skill-creator格式规范。
    检查所有生成物文件，包括 {风格名}* 占位符文件。

    返回：(是否通过, 问题列表)
    """
    issues = []
    skill_md = Path(skill_path) / "SKILL.md"

    if not skill_md.exists():
        return False, ["[FAIL] SKILL.md not found"]

    content = skill_md.read_text(encoding="utf-8")

    # 1. YAML frontmatter 检查
    if not content.startswith("---"):
        issues.append("[FAIL] SKILL.md missing YAML frontmatter")
    else:
        parts = content.split("---", 2)
        if len(parts) < 3:
            issues.append("[FAIL] YAML frontmatter not properly closed")
        else:
            fm_text = parts[1]
            required_fields = ["name", "description"]
            for field in required_fields:
                if field not in fm_text:
                    issues.append(f"[FAIL] frontmatter missing required field: {field}")

    # 2. name 字段规范检查（生成物skill用-writer后缀）
    name_match = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
    if name_match:
        name_value = name_match.group(1).strip()
        if not re.match(r"^[a-z0-9_-]+$", name_value):
            issues.append(f"[FAIL] name field invalid: '{name_value}'")
        if not name_value.endswith("-writer"):
            issues.append(f"[WARN] name should end with '-writer' for generated skill")

    # 3. description 字段检查
    desc_match = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)
    if desc_match:
        desc_value = desc_match.group(1).strip()
        if len(desc_value) > 200:
            issues.append(f"[WARN] description too long ({len(desc_value)} chars)")
    else:
        issues.append("[FAIL] frontmatter missing description")

    # 4. 章节结构检查
    required_sections = [
        ("任务目标", "任务目标|##.*任务"),
        ("操作步骤", "操作步骤|##.*操作"),
        ("注意事项", "注意事项|##.*注意"),
    ]
    for section_name, pattern in required_sections:
        if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            issues.append(f"[FAIL] SKILL.md missing required section: {section_name}")

    # 5. 生成物文件结构检查
    required_files = [
        ("SKILL.md", skill_md),
        ("固化模块/", Path(skill_path) / "固化模块"),
        ("references/", Path(skill_path) / "references"),
        ("scripts/", Path(skill_path) / "scripts"),
    ]
    for name, path in required_files:
        if name.endswith("/"):
            if not path.exists() or not path.is_dir():
                issues.append(f"[FAIL] Missing required directory: {name}")
        else:
            if not path.exists():
                issues.append(f"[FAIL] Missing required file: {name}")

    # 6. references 目录内容检查（生成物文件）
    refs_dir = Path(skill_path) / "references"
    if refs_dir.exists():
        # 生成物必须包含 {风格名}* 文件
        ref_files = list(refs_dir.glob("*"))
        has_placeholder_files = any(
            f.stem != "self_eval" and ("创作风格" in f.stem or "合规" in f.stem or "html" in f.stem)
            for f in ref_files if f.is_file()
        )
        if not has_placeholder_files:
            issues.append("[WARN] references/ missing {风格名}* files (创作风格/合规检查/html海报模板)")

        required_refs = [
            "step1.md",
            "step2.md",
            "step3.md",
            "step4.md",
            "self_eval.md",
        ]
        for ref in required_refs:
            ref_path = refs_dir / ref
            if not ref_path.exists():
                issues.append(f"[FAIL] references/ missing file: {ref}")
            elif ref_path.stat().st_size < 50:
                issues.append(f"[WARN] references/{ref} too small")

    # 7. scripts 目录检查
    scripts_dir = Path(skill_path) / "scripts"
    if scripts_dir.exists():
        if not (scripts_dir / "fetch_market_data.py").exists():
            issues.append("[FAIL] scripts/ missing fetch_market_data.py")

    # 8. 固化模块目录检查
    guding_dir = Path(skill_path) / "固化模块"
    if guding_dir.exists():
        required_guding = ["compliance.md", "market_data.py"]
        for f in required_guding:
            if not (guding_dir / f).exists():
                issues.append(f"[FAIL] 固化模块/ missing: {f}")

    passed = len([i for i in issues if i.startswith("[FAIL]")]) == 0
    return passed, issues


def validate_with_skill_creator(skill_path: str) -> Tuple[bool, List[str]]:
    """
    如果 skill-creator 已安装，调用外部校验。
    否则返回 (True, ["skill-creator 未安装，使用内置校验"])。

    增强的异常处理：
    - ImportError: skill-creator 未安装
    - AttributeError: validate_skill 函数不存在
    - TypeError: 返回格式不符合预期
    - 其他异常: 记录并回退到内置校验
    """
    try:
        from skill_creator import validate_skill
    except ImportError:
        return True, ["skill-creator 未安装，使用内置格式校验"]
    except Exception as e:
        return True, [f"skill-creator 导入异常({type(e).__name__}: {e})，使用内置格式校验"]

    try:
        result = validate_skill(skill_path)

        # 校验返回格式
        if isinstance(result, tuple) and len(result) == 2:
            passed, issues = result
            if isinstance(passed, bool) and isinstance(issues, list):
                return passed, [f"[skill-creator] {i}" for i in issues]

        # 兼容 dict 格式的返回
        if isinstance(result, dict):
            passed = result.get('passed', True)
            issues = result.get('issues', [])
            if isinstance(issues, list):
                return bool(passed), [f"[skill-creator] {i}" for i in issues]

        # 返回格式不符合预期
        return True, [f"skill-creator 返回格式异常({type(result).__name__})，使用内置格式校验"]

    except AttributeError as e:
        return True, [f"skill-creator.validate_skill 不存在({e})，使用内置格式校验"]
    except TypeError as e:
        return True, [f"skill-creator 返回类型错误({e})，使用内置格式校验"]
    except Exception as e:
        # 捕获所有其他异常，避免程序崩溃
        return True, [f"skill-creator 调用异常({type(e).__name__}: {e})，使用内置格式校验"]


def run_format_validation(skill_path: str, mode: str = "auto") -> Dict[str, Any]:
    """
    执行格式校验流程。

    mode:
    - "meta": 元skill自检（检查自身文件结构）
    - "generated": 生成物校验（检查生成物完整结构）
    - "auto": 自动判断（根据是否存在固化模块/判断）
    """
    # 自动判断模式
    if mode == "auto":
        if (Path(skill_path) / "固化模块").exists():
            mode = "generated"
        else:
            mode = "meta"

    print(f"\n{'='*50}")
    print(f"[CHECK] Skill Format Validation ({mode} mode)")
    print(f"{'='*50}")

    # 优先尝试使用外部 skill-creator
    sc_passed, sc_issues = validate_with_skill_creator(skill_path)
    for issue in sc_issues:
        print(f"   {issue}")

    # 内置校验
    if mode == "meta":
        built_in_passed, built_in_issues = validate_meta_skill(skill_path)
        validator_type = "meta-skill"
    else:
        built_in_passed, built_in_issues = validate_generated_skill(skill_path)
        validator_type = "generated-skill"

    for issue in built_in_issues:
        print(f"   {issue}")

    # 如果外部调用失败（包含"使用内置"字样），以内置结果为准
    sc_used_builtin = any("使用内置" in issue for issue in sc_issues) if sc_issues else True
    if sc_used_builtin:
        final_passed = built_in_passed
        final_issues = built_in_issues
        validator = f"builtin ({validator_type})"
    else:
        final_passed = sc_passed and built_in_passed
        final_issues = sc_issues + built_in_issues
        validator = f"skill-creator + builtin ({validator_type})"

    print(f"\n   Validator: {validator}")
    if final_passed:
        print(f"   [PASS] Format validation passed")
    else:
        print(f"   [FAIL] Format validation failed, {len([i for i in final_issues if i.startswith('[FAIL]')])} issues")

    return {
        "passed": final_passed,
        "issues": final_issues,
        "validator": validator,
        "mode": mode,
    }


# ============ 核心函数 ============

def load_skill(skill_path: str) -> Dict[str, Any]:
    """加载生成的Skill"""
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析frontmatter
    frontmatter = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            for line in fm_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()

    return {
        "frontmatter": frontmatter,
        "content": content,
        "path": skill_path,
    }


def load_samples(samples_path: str) -> List[Dict[str, str]]:
    """加载原始案例"""
    samples = []
    path = Path(samples_path)

    if path.is_file():
        # 单文件
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            samples.append({
                "content": content,
                "path": str(path),
                "title": extract_title(content),
            })
    else:
        # 文件夹
        for md_file in sorted(path.glob("*.md")):
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                samples.append({
                    "content": content,
                    "path": str(md_file),
                    "title": extract_title(content),
                })

    return samples


def extract_title(text: str) -> str:
    """从文章中提取标题"""
    # 匹配【】标题
    match = re.search(r"【([^】]+)】", text)
    if match:
        return match.group(0)
    # 匹配第一行markdown标题
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if match:
        return match.group(1)
    return "未识别标题"


def extract_dimension(text: str, dimension: str) -> Dict[str, Any]:
    """提取指定维度的特征"""
    extractors = {
        "标题格式": extract_title_format,
        "段落结构": extract_paragraph_structure,
        "句式特征": extract_sentence_features,
        "特色词汇": extract_vocabulary,
        "分析逻辑": extract_analysis_logic,
        "固定表达": extract_fixed_expressions,
    }

    extractor = extractors.get(dimension, lambda x: {})
    return extractor(text)


def extract_title_format(text: str) -> Dict[str, Any]:
    """提取标题格式"""
    # 匹配【】标题
    titles = re.findall(r"【([^】]+)】", text)
    has_brackets = len(titles) > 0

    # 检查标题格式特征
    has_副标题 = "——" in text or "--" in text

    # 标题长度
    title_lengths = [len(t) for t in titles]

    return {
        "count": len(titles),
        "examples": titles[:3],
        "has_brackets": has_brackets,
        "has_subtitle": has_副标题,
        "avg_length": sum(title_lengths) / len(title_lengths) if title_lengths else 0,
        "titles": titles,
    }


def extract_paragraph_structure(text: str) -> Dict[str, Any]:
    """提取段落结构"""
    # 按换行分割段落，过滤空段落
    paragraphs = [p.strip() for p in text.split("\n") if p.strip() and len(p.strip()) > 10]

    # 统计每段长度
    lengths = [len(p) for p in paragraphs]

    # 检查是否有固定开头语
    opening_patterns = [
        r"^昨日",
        r"^今日",
        r"^近期",
        r"^走势",
        r"^操作",
        r"^鱼群",
        r"^关联",
    ]

    fixed_openings = []
    for p in paragraphs[:6]:
        for pattern in opening_patterns:
            if re.search(pattern, p):
                fixed_openings.append(pattern.replace("^", ""))
                break

    return {
        "count": len(paragraphs),
        "avg_length": sum(lengths) / len(lengths) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "fixed_openings": fixed_openings,
    }


def extract_sentence_features(text: str) -> Dict[str, Any]:
    """提取句式特征"""
    # 统计分号、冒号使用
    semicolons = text.count("；")
    colons = text.count("：")

    # 条件判断句
    conditional_patterns = [
        r"若.*则",
        r"若没有",
        r"大概率",
        r"或许",
        r"可能要",
        r"倾向于",
    ]
    conditionals = sum(len(re.findall(p, text)) for p in conditional_patterns)

    # 概率性表达
    probability_words = ["大概率", "或许", "可能", "倾向于", "值得关注", "有望"]
    probabilities = sum(text.count(w) for w in probability_words)

    # 句子平均长度（简化：按句号和感叹号分割）
    sentences = re.split(r"[。！？]", text)
    sentence_lengths = [len(s) for s in sentences if s.strip()]

    return {
        "semicolons": semicolons,
        "colons": colons,
        "conditionals": conditionals,
        "probabilities": probabilities,
        "avg_sentence_length": sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
    }


def extract_vocabulary(text: str) -> Dict[str, Any]:
    """提取特色词汇"""
    # 比喻词（金融领域常用比喻）
    metaphor_words = [
        "鱼群", "鲸鱼", "压舱石", "资金流", "板块轮动",
        "跷跷板", "风向标", "领头羊", "国家队", "庄家",
    ]
    found_metaphors = [w for w in metaphor_words if w in text]

    # 谨慎词
    caution_words = ["大概率", "或许", "可能", "建议", "倾向于", "值得关注", "有望", "或"]
    found_cautions = [w for w in caution_words if w in text]

    # 专业术语
    professional_words = [
        "缩量", "放量", "震荡", "轮动", "催化", "避险",
        "高低切换", "防御性", "量价齐升", "突破", "支撑位", "压力位",
    ]
    found_professional = [w for w in professional_words if w in text]

    # 禁止词（合规红线）
    forbidden_words = ["暴涨", "暴跌", "肯定", "绝对", "必然", "必将", "推荐买入"]
    found_forbidden = [w for w in forbidden_words if w in text]

    return {
        "metaphors": found_metaphors,
        "cautions": found_cautions,
        "professional": found_professional,
        "forbidden": found_forbidden,
        "metaphor_count": len(found_metaphors),
        "caution_count": len(found_cautions),
    }


def extract_analysis_logic(text: str) -> Dict[str, Any]:
    """提取分析逻辑"""
    # 分析框架关键词（数据→事件→逻辑→结论→建议）
    framework_keywords = {
        "数据": ["数据", "成交额", "涨跌幅", "指数", "资金"],
        "事件": ["事件", "政策", "会议", "数据发布", "外围"],
        "逻辑": ["逻辑", "因", "所以", "导致", "利好", "利空"],
        "结论": ["结论", "总之", "整体来看", "大概率", "预计"],
        "建议": ["建议", "操作", "关注", "配置", "仓位"],
    }

    found_framework = {}
    for category, keywords in framework_keywords.items():
        found_framework[category] = sum(text.count(k) for k in keywords)

    # 转折词
    transition_words = ["然而", "但", "不过", "虽然", "尽管", "然而"]
    transitions = [w for w in transition_words if w in text]

    # 段落结构关键词
    section_keywords = {
        "市场概述": ["昨日", "今日", "市场", "震荡", "上涨", "下跌"],
        "事件分析": ["事件", "政策", "近期", "层面"],
        "外围市场": ["美股", "港股", "外围", "关联"],
        "技术分析": ["走势", "结构", "支撑", "压力", "突破"],
        "资金流向": ["鱼群", "资金", "板块", "流入", "流出"],
        "操作建议": ["操作", "建议", "仓位", "关注"],
    }

    section_presence = {}
    for section, keywords in section_keywords.items():
        section_presence[section] = sum(text.count(k) for k in keywords) > 0

    return {
        "framework_keywords": found_framework,
        "transitions": transitions,
        "section_presence": section_presence,
        "transition_count": len(transitions),
    }


def extract_fixed_expressions(text: str) -> Dict[str, Any]:
    """提取固定表达"""
    # 段落开头语（前6段）
    paragraphs = [p.strip() for p in text.split("\n") if p.strip() and len(p.strip()) > 10]
    opening_phrases = []
    for p in paragraphs[:6]:
        # 取前20个字符作为开头语
        phrase = p[:20].strip()
        opening_phrases.append(phrase)

    # 检查固定格式
    fixed_patterns = {
        "风险提示": ["仅供参考", "风险自担", "市场有风险"],
        "签约呼号": ["签约", "股票池", "解锁"],
        "概率表达": ["大概率", "或许", "可能", "倾向于"],
    }

    found_fixed = {}
    for name, patterns in fixed_patterns.items():
        found_fixed[name] = any(any(p in text for p in patterns),)

    return {
        "opening_phrases": opening_phrases,
        "has_risk_disclaimer": found_fixed.get("风险提示", False),
        "has_branding": found_fixed.get("签约呼号", False),
        "has_probability_expr": found_fixed.get("概率表达", False),
    }


def compare_dimensions(
    generated: Dict[str, Any],
    reference: Dict[str, Any],
    dimension: str
) -> Tuple[float, List[str]]:
    """对比单一维度，返回（匹配度, 差距列表）"""
    gaps = []

    if dimension == "标题格式":
        ref_has_brackets = reference.get("has_brackets", False)
        gen_has_brackets = generated.get("has_brackets", False)
        score = 1.0 if ref_has_brackets == gen_has_brackets else 0.5

        if ref_has_brackets:
            ref_titles = set(reference.get("titles", []))
            gen_titles = set(generated.get("titles", []))
            if ref_titles and gen_titles:
                title_overlap = len(ref_titles & gen_titles) / len(ref_titles)
                score = (score + title_overlap) / 2

        ref_subtitle = reference.get("has_subtitle", False)
        gen_subtitle = generated.get("has_subtitle", False)
        if ref_subtitle != gen_subtitle:
            gaps.append(f"副标题格式不一致")

    elif dimension == "段落结构":
        ref_count = reference.get("count", 0)
        gen_count = generated.get("count", 0)

        if ref_count > 0:
            # 段落数量匹配度
            count_score = min(gen_count, ref_count) / max(gen_count, ref_count)
            # 平均长度匹配度
            ref_avg = reference.get("avg_length", 0)
            gen_avg = generated.get("avg_length", 0)
            if ref_avg > 0 and gen_avg > 0:
                len_score = min(gen_avg, ref_avg) / max(gen_avg, ref_avg)
            else:
                len_score = 0.8
            score = (count_score * 0.6 + len_score * 0.4)
        else:
            score = 0.5

        if abs(gen_count - ref_count) > 2:
            gaps.append(f"段落数量差异大: 生成{gen_count}段 vs 案例{ref_count}段")
        elif abs(gen_count - ref_count) > 1:
            gaps.append(f"段落数量略有差异: 生成{gen_count}段 vs 案例{ref_count}段")

    elif dimension == "句式特征":
        # 检查条件句和概率表达
        ref_cond = reference.get("conditionals", 0) + reference.get("probabilities", 0)
        gen_cond = generated.get("conditionals", 0) + generated.get("probabilities", 0)

        if ref_cond > 0:
            score = min(gen_cond, ref_cond) / max(gen_cond, ref_cond)
        else:
            score = 0.8

        # 检查分号使用（专业度指标）
        ref_semi = reference.get("semicolons", 0)
        gen_semi = generated.get("semicolons", 0)
        if ref_semi > 0:
            semi_score = min(gen_semi, ref_semi) / max(gen_semi, ref_semi)
            score = (score + semi_score) / 2

        score = max(0.5, min(1.0, score))

        if gen_cond < ref_cond * 0.5:
            gaps.append(f"条件句/概率表达不足: 生成{gen_cond}处 vs 案例{ref_cond}处")

    elif dimension == "特色词汇":
        ref_mets = set(reference.get("metaphors", []))
        gen_mets = set(generated.get("metaphors", []))
        ref_cautions = set(reference.get("cautions", []))
        gen_cautions = set(generated.get("cautions", []))

        # 比喻词匹配
        if ref_mets:
            metaphor_score = len(gen_mets & ref_mets) / len(ref_mets)
        else:
            metaphor_score = 1.0

        # 谨慎词匹配
        if ref_cautions:
            caution_score = len(gen_cautions & ref_cautions) / len(ref_cautions)
        else:
            caution_score = 0.8

        score = (metaphor_score * 0.4 + caution_score * 0.6)

        if gen_mets - ref_mets:
            gaps.append(f"多余比喻词: {gen_mets - ref_mets}")
        missing_mets = ref_mets - gen_mets
        if missing_mets:
            gaps.append(f"缺少比喻词: {missing_mets}")

        # 检查禁止词
        if generated.get("forbidden", []):
            gaps.append(f"使用了禁止词: {generated.get('forbidden', [])}")

    elif dimension == "分析逻辑":
        ref_framework = reference.get("framework_keywords", {})
        gen_framework = generated.get("framework_keywords", {})

        # 计算框架关键词覆盖率
        ref_total = sum(ref_framework.values())
        gen_total = sum(gen_framework.values())

        if ref_total > 0:
            score = min(gen_total, ref_total) / max(gen_total, ref_total)
        else:
            score = 0.7

        # 检查段落结构完整性
        ref_sections = reference.get("section_presence", {})
        gen_sections = generated.get("section_presence", {})
        if ref_sections and gen_sections:
            ref_complete = sum(1 for v in ref_sections.values() if v)
            gen_complete = sum(1 for v in gen_sections.values() if v)
            if ref_complete > 0:
                section_score = gen_complete / ref_complete
                score = (score + section_score) / 2

        if generated.get("transition_count", 0) < 1:
            gaps.append("缺少转折词使用")

    elif dimension == "固定表达":
        ref_phrases = generated.get("opening_phrases", [])
        gen_phrases = generated.get("opening_phrases", [])

        if ref_phrases and gen_phrases:
            # 开头语匹配度
            matches = sum(1 for g, r in zip(gen_phrases, ref_phrases) if g == r)
            score = max(0.3, matches / len(ref_phrases))
        else:
            score = 0.7

        ref_has_risk = reference.get("has_risk_disclaimer", False)
        gen_has_risk = generated.get("has_risk_disclaimer", False)
        ref_has_branding = reference.get("has_branding", False)
        gen_has_branding = generated.get("has_branding", False)

        if ref_has_risk and not gen_has_risk:
            gaps.append("缺少风险提示")
        if ref_has_branding and not gen_has_branding:
            gaps.append("缺少品牌呼号")

    else:
        score = 0.7
        gaps.append(f"未知维度: {dimension}")

    return score, gaps


def merge_reference_features(features_list: List[Dict]) -> Dict:
    """合并多篇案例的特征（取共识）"""
    merged = {}

    for dim in DIMENSION_WEIGHTS.keys():
        dim_features = [f.get(dim, {}) for f in features_list]

        # 对于每个维度，合并多个样本的特征
        if dim == "标题格式":
            # 取所有样本的共同特征
            all_titles = []
            for feat in dim_features:
                all_titles.extend(feat.get("titles", []))
            if all_titles:
                merged[dim] = {
                    "has_brackets": any(f.get("has_brackets", False) for f in dim_features),
                    "has_subtitle": any(f.get("has_subtitle", False) for f in dim_features),
                    "titles": list(set(all_titles)),
                }
            else:
                merged[dim] = {}

        elif dim == "段落结构":
            counts = [f.get("count", 0) for f in dim_features if f.get("count", 0) > 0]
            avg_lengths = [f.get("avg_length", 0) for f in dim_features if f.get("avg_length", 0) > 0]

            # 取中位数
            merged[dim] = {
                "count": sorted(counts)[len(counts)//2] if counts else 0,
                "avg_length": sum(avg_lengths) / len(avg_lengths) if avg_lengths else 0,
            }

        elif dim == "句式特征":
            merged[dim] = {
                "conditionals": sum(f.get("conditionals", 0) for f in dim_features) // max(1, len(dim_features)),
                "probabilities": sum(f.get("probabilities", 0) for f in dim_features) // max(1, len(dim_features)),
                "semicolons": sum(f.get("semicolons", 0) for f in dim_features) // max(1, len(dim_features)),
            }

        elif dim == "特色词汇":
            all_metaphors = []
            all_cautions = []
            for feat in dim_features:
                all_metaphors.extend(feat.get("metaphors", []))
                all_cautions.extend(feat.get("cautions", []))

            # 出现≥50%样本的词汇
            threshold = len(dim_features) * 0.5
            metaphor_counts = {}
            for m in all_metaphors:
                metaphor_counts[m] = metaphor_counts.get(m, 0) + 1
            final_metaphors = [k for k, v in metaphor_counts.items() if v >= threshold]

            caution_counts = {}
            for c in all_cautions:
                caution_counts[c] = caution_counts.get(c, 0) + 1
            final_cautions = [k for k, v in caution_counts.items() if v >= threshold]

            merged[dim] = {
                "metaphors": list(set(final_metaphors)),
                "cautions": list(set(final_cautions)),
            }

        elif dim == "分析逻辑":
            merged_framework = {}
            for feat in dim_features:
                for k, v in feat.get("framework_keywords", {}).items():
                    merged_framework[k] = merged_framework.get(k, 0) + v

            all_transitions = []
            for feat in dim_features:
                all_transitions.extend(feat.get("transitions", []))

            merged_sections = {}
            for feat in dim_features:
                for k, v in feat.get("section_presence", {}).items():
                    if k not in merged_sections:
                        merged_sections[k] = 0
                    merged_sections[k] += (1 if v else 0)

            # 超过50%样本有的段落结构
            threshold = len(dim_features) * 0.5
            final_sections = {k: v >= threshold for k, v in merged_sections.items()}

            merged[dim] = {
                "framework_keywords": merged_framework,
                "transitions": list(set(all_transitions)),
                "section_presence": final_sections,
                "transition_count": len(set(all_transitions)),
            }

        elif dim == "固定表达":
            merged[dim] = {
                "has_risk_disclaimer": any(f.get("has_risk_disclaimer", False) for f in dim_features),
                "has_branding": any(f.get("has_branding", False) for f in dim_features),
                "has_probability_expr": any(f.get("has_probability_expr", False) for f in dim_features),
                "opening_phrases": dim_features[0].get("opening_phrases", []) if dim_features else [],
            }

        else:
            merged[dim] = dim_features[0] if dim_features else {}

    return merged


def generate_recommendations(scores: Dict[str, float], gaps: List[str]) -> List[str]:
    """生成修复建议"""
    recommendations = []

    for dim, score in scores.items():
        if score < MIN_DIMENSION_SCORE:
            recommendations.append(f"【{dim}】得分{score:.1%}过低(<50%)，必须重点修复")
        elif score < ACCEPTANCE_THRESHOLD:
            recommendations.append(f"【{dim}】得分{score:.1%}未达标(<80%)，有提升空间")

    if gaps:
        recommendations.append(f"具体差距: {'; '.join(gaps)}")

    if not recommendations:
        recommendations.append("整体表现良好，建议维持现有风格")

    return recommendations


def run_self_eval(
    skill_path: str,
    samples_path: str,
    test_topic: str,
    generated_article: Optional[str] = None,
    output_path: str = "eval_report.json"
) -> Dict[str, Any]:
    """执行完整自测评流程"""

    print(f"📊 投顾写作Skill自测评")
    print(f"{'=' * 50}")
    print(f"Skill路径: {skill_path}")
    print(f"案例路径: {samples_path}")
    print(f"测试主题: {test_topic}")
    print()

    # 1. 加载数据
    print(f"[1/5] 加载数据和Skill...")
    skill_data = load_skill(skill_path)
    samples = load_samples(samples_path)
    print(f"   Skill: {skill_data['frontmatter'].get('name', '未命名')}")
    print(f"   加载了 {len(samples)} 篇案例")

    # 2. 提取案例特征（作为基准）
    print(f"\n[2/5] 提取案例基准特征...")
    reference_features = []
    for i, sample in enumerate(samples):
        features = {}
        for dim in DIMENSION_WEIGHTS.keys():
            features[dim] = extract_dimension(sample["content"], dim)
        reference_features.append(features)
        print(f"   案例{i+1} [{sample.get('title', '未识别')[:20]}...] 特征提取完成")

    # 合并多篇案例的特征（取共识）
    reference = merge_reference_features(reference_features)
    print(f"   特征整合完成（取多篇共识）")

    # 3. 处理生成的测试文章
    print(f"\n[3/5] 处理测试文章...")
    if not generated_article:
        print(f"   ⚠️ 警告: 未提供生成的文章内容")
        print(f"   请使用生成的Skill撰写一篇关于'{test_topic}'的文章")
        print(f"   然后将文章内容传递给 --generated-article 参数重新运行")
        print(f"   示例:")
        print(f"   python self_eval.py --skill-path . --reference-samples ./samples --test-topic '今日收评' --generated-article '@generated_article.txt' ...")
        generated_features = {}
        for dim in DIMENSION_WEIGHTS.keys():
            generated_features[dim] = {}
    else:
        # 如果generated_article是文件路径，读取文件
        if os.path.isfile(generated_article):
            with open(generated_article, "r", encoding="utf-8") as f:
                generated_article = f.read()
            print(f"   已从文件读取生成文章 ({len(generated_article)} 字符)")

        # 提取生成文章的特征
        generated_features = {}
        for dim in DIMENSION_WEIGHTS.keys():
            generated_features[dim] = extract_dimension(generated_article, dim)
        print(f"   测试文章特征提取完成 ({len(generated_article)} 字符)")

    # 4. 7维对比分析
    print(f"\n[4/5] 7维对比分析...")
    dimension_scores = {}
    all_gaps = []

    for dim in DIMENSION_WEIGHTS.keys():
        gen_feat = generated_features.get(dim, {})
        ref_feat = reference.get(dim, {})
        score, gaps = compare_dimensions(gen_feat, ref_feat, dim)
        dimension_scores[dim] = score
        all_gaps.extend(gaps)

        status = "✅" if score >= ACCEPTANCE_THRESHOLD else ("⚠️" if score >= MIN_DIMENSION_SCORE else "❌")
        print(f"   {status} {dim}: {score:.1%}")

    # 计算整体得分
    overall_score = sum(
        dimension_scores[dim] * weight
        for dim, weight in DIMENSION_WEIGHTS.items()
    )

    print(f"\n   整体匹配度: {overall_score:.1%}")

    # 5. 生成报告
    print(f"\n[5/5] 生成测评报告...")
    report = {
        "timestamp": datetime.now().isoformat(),
        "skill_path": skill_path,
        "samples_path": samples_path,
        "test_topic": test_topic,
        "overall_score": overall_score,
        "dimension_scores": dimension_scores,
        "dimension_weights": DIMENSION_WEIGHTS,
        "gaps": all_gaps,
        "passed": overall_score >= ACCEPTANCE_THRESHOLD,
        "recommendations": generate_recommendations(dimension_scores, all_gaps),
        "reference_summary": {
            "sample_count": len(samples),
            "titles": [s.get("title", "未识别") for s in samples],
        },
    }

    # 保存报告
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"📋 测评报告已保存到: {output_path}")

    if report["passed"]:
        print(f"✅ 整体匹配度 {overall_score:.1%} ≥ {ACCEPTANCE_THRESHOLD:.1%}，通过！")
    else:
        print(f"❌ 整体匹配度 {overall_score:.1%} < {ACCEPTANCE_THRESHOLD:.1%}，需修复")

    print(f"\n📝 修复建议:")
    for rec in report["recommendations"]:
        print(f"   - {rec}")

    return report


# ============ CLI入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="投顾写作Skill自测评辅助工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 仅格式校验（skill-creator规范）
  python self_eval.py --skill-path ./收评writer --validate-format-only

  # 仅风格对比（需先准备好样本和生成的文章）
  python self_eval.py --skill-path ./收评writer --reference-samples ./samples --compare-style-only

  # 完整流程（需要提供生成的文章）
  python self_eval.py --skill-path ./收评writer --reference-samples ./samples --test-topic "今日收评" --generated-article "生成的测试文章..."

  # 提供生成的文章文件
  python self_eval.py --skill-path ./收评writer --reference-samples ./samples --test-topic "今日收评" --generated-article ./test_article.txt --output ./eval_report.json
        """
    )
    parser.add_argument("--skill-path", required=True, help="生成的Skill路径")
    parser.add_argument("--validate-format-only", action="store_true", help="仅执行格式校验（skill-creator规范）")
    parser.add_argument("--meta-skill", action="store_true", help="将skill-path作为元skill进行自检")
    parser.add_argument("--compare-style-only", action="store_true", help="仅执行7维度风格对比")
    parser.add_argument("--reference-samples", default=None, help="原始案例路径（文件或文件夹）")
    parser.add_argument("--test-topic", default=None, help="测试主题（如'今日收评'）")
    parser.add_argument("--generated-article", default=None, help="生成的测试文章（文件路径或直接内容）")
    parser.add_argument("--output", default="eval_report.json", help="报告输出路径")

    args = parser.parse_args()

    try:
        # 仅格式校验模式
        if args.validate_format_only:
            mode = "meta" if args.meta_skill else "auto"
            result = run_format_validation(args.skill_path, mode=mode)
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\nFormat validation report saved: {args.output}")
            exit(0 if result["passed"] else 1)

        # 仅风格对比模式
        if args.compare_style_only:
            if not args.reference_samples:
                print("❌ 错误: --compare-style-only 需要 --reference-samples")
                exit(2)
            report = run_self_eval(
                args.skill_path,
                args.reference_samples,
                args.test_topic or "风格对比测试",
                args.generated_article,
                args.output
            )
            exit(0 if report.get("passed", False) else 1)

        # 完整流程模式
        if not args.reference_samples or not args.test_topic:
            print("❌ 错误: 完整流程需要 --reference-samples 和 --test-topic")
            print("   或使用 --validate-format-only 仅做格式校验")
            exit(2)

        report = run_self_eval(
            args.skill_path,
            args.reference_samples,
            args.test_topic,
            args.generated_article,
            args.output
        )

        # 返回退出码
        exit(0 if report.get("passed", False) else 1)

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        exit(2)


if __name__ == "__main__":
    main()
