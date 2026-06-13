<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Agent Skills Factory</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #24292e; background: #f6f8fa; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 40px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .lang-switch { display: flex; justify-content: center; gap: 10px; padding: 20px; background: #f6f8fa; border-bottom: 1px solid #e1e4e8; }
        .lang-btn { padding: 10px 30px; border: 2px solid #667eea; background: #fff; color: #667eea; border-radius: 25px; cursor: pointer; font-weight: 600; transition: all 0.3s; }
        .lang-btn:hover { background: #667eea; color: #fff; }
        .lang-btn.active { background: #667eea; color: #fff; }
        .content { padding: 40px; }
        .content[lang="en"] { display: none; }
        h2 { color: #667eea; margin: 30px 0 15px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }
        h3 { color: #333; margin: 20px 0 10px; }
        p { margin: 15px 0; }
        ul { margin: 15px 0; padding-left: 25px; }
        li { margin: 8px 0; }
        code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-family: Monaco, monospace; color: #e74c3c; }
        pre { background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 8px; overflow-x: auto; margin: 15px 0; font-size: 14px; }
        pre code { background: none; color: inherit; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { border: 1px solid #e1e4e8; padding: 12px; text-align: left; }
        th { background: #667eea; color: #fff; }
        tr:nth-child(even) { background: #f6f8fa; }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin: 2px; }
        .badge-primary { background: #667eea; color: #fff; }
        .badge-success { background: #27ae60; color: #fff; }
        .footer { text-align: center; padding: 30px; color: #666; border-top: 1px solid #e1e4e8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Multi-Agent Skills Factory</h1>
            <p>多Agent协作SOP封装流水线 | Multi-Agent SOP Packaging Pipeline</p>
        </div>
        <div class="lang-switch">
            <button class="lang-btn active" onclick="switchLang('zh')">中文</button>
            <button class="lang-btn" onclick="switchLang('en')">English</button>
        </div>
        <div class="content" lang="zh">
            <h2>概述</h2>
            <p>Multi-Agent Skills Factory 是一个将企业SOP流程封装为可复用Hermes Skill的自动化工作流。通过主编调度6个专业Agent并行协作，实现从业务流程到AI技能的端到端转化。</p>
            <h3>核心特性</h3>
            <ul>
                <li>主编智能调度，多Agent并行工作</li>
                <li>自动化评分迭代，达标（≥75分）才上线</li>
                <li>完整测试用例池，保证交付质量</li>
            </ul>
            <h2>Agent团队</h2>
            <table>
                <tr><th>Agent</th><th>输出</th><th>职责</th></tr>
                <tr><td>主编</td><td>任务调度+最终交付</td><td>解析需求、分解任务、协调Agent、组装产出</td></tr>
                <tr><td>研究员</td><td>SOP分析报告</td><td>深度理解业务流程、提取关键节点、识别边界场景</td></tr>
                <tr><td>设计师</td><td>技能设计规格书</td><td>触发词设计、流程建模、输入输出定义</td></tr>
                <tr><td>开发者</td><td>SKILL.md代码</td><td>按hermes-agent-skill-authoring标准编写代码</td></tr>
                <tr><td>测试员</td><td>测试报告</td><td>语法验证、功能测试、边界测试、安全测试</td></tr>
                <tr><td>评审员</td><td>评审报告</td><td>五维打分（完整性/正确性/易用性/安全性/可维护性）</td></tr>
            </table>
            <h2>评审维度</h2>
            <table>
                <tr><th>维度</th><th>分值</th><th>说明</th></tr>
                <tr><td>完整性</td><td>20分</td><td>核心流程是否覆盖完整SOP</td></tr>
                <tr><td>正确性</td><td>20分</td><td>输出结果是否符合hermes-agent-skill-authoring标准</td></tr>
                <tr><td>易用性</td><td>20分</td><td>触发词是否清晰、使用是否简单</td></tr>
                <tr><td>安全性</td><td>20分</td><td>是否有敏感信息泄露风险</td></tr>
                <tr><td>可维护性</td><td>20分</td><td>代码结构是否清晰、references/是否规范</td></tr>
            </table>
            <h2>评分规则</h2>
            <ul>
                <li><span class="badge badge-success">≥90分</span> 优秀，直接上线</li>
                <li><span class="badge badge-primary">75-89分</span> 良好，小修小补后上线</li>
                <li><span class="badge badge-primary"><75分</span> 退回开发者修改，最多6轮</li>
            </ul>
            <h2>触发词</h2>
            <ul>
                <li>"把这个流程封装成Skill"</li>
                <li>"建一个处理XX的技能"</li>
                <li>"SOP太重复了，做成自动化"</li>
                <li><code>/封装Skill [SOP描述]</code></li>
            </ul>
            <h2>目录结构</h2>
            <pre><code>multi-agent-skills-factory/
├── SKILL.md
└── references/
    ├── agents.md
    ├── pipeline-multi-agent.md
    ├── design-spec-template.md
    ├── eval-dimensions.md
    └── test_pool.md</code></pre>
        </div>
        <div class="content" lang="en">
            <h2>Overview</h2>
            <p>Multi-Agent Skills Factory is an automated workflow that packages enterprise SOP processes into reusable Hermes Skills. Through an Editor-in-Chief orchestrating 6 specialized agents working in parallel, it achieves end-to-end transformation from business processes to AI skills.</p>
            <h3>Core Features</h3>
            <ul>
                <li>Editor-in-Chief intelligent scheduling, multi-agent parallel work</li>
                <li>Automated scoring iteration, only goes live when score ≥75</li>
                <li>Complete test suite, ensuring delivery quality</li>
            </ul>
            <h2>Agent Team</h2>
            <table>
                <tr><th>Agent</th><th>Output</th><th>Responsibilities</th></tr>
                <tr><td>Editor-in-Chief</td><td>Task scheduling + final delivery</td><td>Parse requirements, decompose tasks, coordinate agents, assemble output</td></tr>
                <tr><td>Researcher</td><td>SOP analysis report</td><td>Deep understanding of business process, extract key nodes, identify edge cases</td></tr>
                <tr><td>Designer</td><td>Skill design specification</td><td>Trigger word design, process modeling, input/output definition</td></tr>
                <tr><td>Developer</td><td>SKILL.md code</td><td>Write code according to hermes-agent-skill-authoring standards</td></tr>
                <tr><td>Tester</td><td>Test report</td><td>Syntax verification, functional testing, boundary testing, security testing</td></tr>
                <tr><td>Reviewer</td><td>Review report</td><td>Five-dimensional scoring (completeness/correctness/usability/security/maintainability)</td></tr>
            </table>
            <h2>Review Dimensions</h2>
            <table>
                <tr><th>Dimension</th><th>Score</th><th>Description</th></tr>
                <tr><td>Completeness</td><td>20pts</td><td>Does the core process cover the complete SOP?</td></tr>
                <tr><td>Correctness</td><td>20pts</td><td>Does the output meet hermes-agent-skill-authoring standards?</td></tr>
                <tr><td>Usability</td><td>20pts</td><td>Are trigger words clear and usage simple?</td></tr>
                <tr><td>Security</td><td>20pts</td><td>Any risk of sensitive information leakage?</td></tr>
                <tr><td>Maintainability</td><td>20pts</td><td>Is the code structure clear, references/ organized?</td></tr>
            </table>
            <h2>Scoring Rules</h2>
            <ul>
                <li><span class="badge badge-success">≥90pts</span> Excellent, go live directly</li>
                <li><span class="badge badge-primary">75-89pts</span> Good, go live after minor fixes</li>
                <li><span class="badge badge-primary"><75pts</span> Return to developer, max 6 rounds</li>
            </ul>
            <h2>Trigger Words</h2>
            <ul>
                <li>"Package this process as a Skill"</li>
                <li>"Build a skill for handling XX"</li>
                <li>"SOP is too repetitive, make it automated"</li>
                <li><code>/packageSkill [SOP description]</code></li>
            </ul>
            <h2>Directory Structure</h2>
            <pre><code>multi-agent-skills-factory/
├── SKILL.md
└── references/
    ├── agents.md
    ├── pipeline-multi-agent.md
    ├── design-spec-template.md
    ├── eval-dimensions.md
    └── test_pool.md</code></pre>
        </div>
        <div class="footer">
            <p>Multi-Agent Skills Factory | MIT License</p>
        </div>
    </div>
    <script>
        function switchLang(lang) {
            document.querySelectorAll('.content').forEach(el => {
                el.style.display = el.getAttribute('lang') === lang ? 'block' : 'none';
            });
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }
    </script>
</body>
</html>