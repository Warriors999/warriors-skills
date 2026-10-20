# AI 视频文字安全工作流：资料依据

核查日期：2026-09-16

这些资料用于支持工作流判断，不代表任何单一平台能够保证逐帧准确的中文文字。

## Codex / Skill 写法

- [OpenAI Codex](https://developers.openai.com/codex)：官方 Codex 入口，当前页面结构可能随版本变化。
- 本机 `skill-creator` 与 `writing-skills`：Skill 元数据、触发描述、渐进式披露、测试用例和验证要求。

## 即梦 / Seedance

- [【即梦】Seedance 2.5 使用手册](https://bytedance.larkoffice.com/wiki/RXh5ww6EqighMdkVTMccm2d4n7e)：提示词结构与素材职责的当前参考。具体素材数量、参数和能力仍需以当前界面为准。
- 即梦相关结论只采用“素材职责、动作/镜头/时间结构、保持项和禁止项”等可迁移原则；不把第三方接口字段当作即梦官方语法。

## 专业后期与跟踪

- [Adobe 3D Camera Tracker](https://helpx.adobe.com/after-effects/using/3d-camera-tracker.html)：用于从视频分析摄像机运动并将图层放入 3D 空间。
- [Adobe Motion Tracking](https://helpx.adobe.com/after-effects/using/tracking-stabilizing-motion.html)：AE 的运动跟踪与稳定工作流入口。
- [Adobe Content-Aware Fill](https://helpx.adobe.com/after-effects/using/content-aware-fill.html)：用于视频中不需要内容的清理和填充。
- [Boris FX Mocha Pro](https://borisfx.com/products/mocha-pro/)：官方页面列出平面跟踪、3D 跟踪、Roto、物体移除、PowerMesh 有机变形跟踪；当前页面还介绍 2026.5 的 Point Track ML 与遮挡场景。
- [Blackmagic Design Fusion](https://www.blackmagicdesign.com/products/fusion)：节点式合成、跟踪、遮罩和视觉特效的专业替代路线。

## 相关公开 Agent Skill

- [HyperFrames Student Kit](https://github.com/nateherkai/hyperframes-student-kit)：Codex/Claude Code 视频剪辑与 motion-graphics 工具包；侧重视频工程和动效模板，不是本技能的文字保真/AI 底板路由。
- [Vox AI Motion Graphics Generator](https://github.com/Anil-matcha/vox-ai-motion-graphics-generator)：Agent Skill 形式的 AI 动效视频生成项目；侧重自动化解释视频，不是本技能的 AE 空间文字合成方案。
- [bang-motion](https://github.com/bangtutorial/bang-motion)：面向浏览器动效的 Agent Skill；可参考技能组织方式，但不作为 AE/即梦规则来源。

## 结论

未找到一份同时覆盖“精确中文文字、AI 图生视频、无文字底板、AE 空间跟踪和最终验收”的现成 Codex Skill。因此本技能将：

1. 采用 Skill 的通用触发与渐进式披露结构；
2. 采用即梦资料中的素材职责和提示词分层；
3. 采用 Adobe/Mocha/Fusion 的后期跟踪、清理、遮挡和合成路线；
4. 把平台未知能力明确标为需要重新核验。

## 2026-09-16 新增核查：动态文字不是普通图生视频的可靠能力

- [Text-Animator: Controllable Visual Text Video Generation](https://arxiv.org/abs/2406.17777)：研究论文明确指出，当前 T2V 方法仍难以直接有效生成视频文字，主要问题包括文字保真度和运动连贯性；其项目页还展示了 Gen-2、Open-Sora、Pika 等方法在指定单词上的对比。
- [Kinetic Typography Diffusion Model](https://arxiv.org/abs/2407.10476)：将可读字形、运动效果和视觉外观视为需要专门约束的三个目标，说明普通视频模型提示词不是等价替代。
- [Dynamic Typography: Bringing Text to Life via Video Diffusion Prior](https://arxiv.org/abs/2404.11614)：通过矢量字形、逐帧运动和形状保持机制维持动态文字结构。
- [VideoAny: How to Stop AI Image-to-Video from Warping Your Character](https://videoany.io/blog/posts/how-to-stop-ai-image-to-video-from-warping-your-character)：创作者工作流建议清晰输入、单一小动作、分离主体运动和镜头运动、降低背景复杂度。
- [ClipTrend: AI Image-to-Video Common Mistakes and Fixes](https://cliptrend.ai/blog/ai-image-to-video-mistakes-and-fixes)：将文字和细节列为容易乱码或变形的区域，建议清晰输入、匹配画幅、一次只要求一个主要动作。
- [B 站：全网独家！一招教你解决 AI 文字错乱问题](https://www.bilibili.com/video/BV1e88c6iEs8)：创作者将少量文字分为“修正关键帧后作为视觉锚点”和“文字较多时平面跟踪替换”两种路线，并明确提到透视、运动模糊、明暗、反光和颗粒匹配。
- [B 站：AI 出废片？教你一招搞定视频文字乱码](https://www.bilibili.com/video/BV1ST5g6EErz)：公开教程标题直接针对 AI 视频文字乱码，作为用户实践存在性的佐证；由于页面未提供可核验正文，不能单独作为技术结论。

### 对本 Skill 的影响

“完整文字版 → 无文字版 → 无文字版主参考”不能再作为无条件默认链路。应根据用户实测和文字／效果优先级路由：

1. 效果优先：完整文字版主参考，无文字版为备选或对照；
2. 文字安全：无文字效果版主参考；
3. 少量文字锚点：修正代表性关键帧，仅在平台支持时用于视频编辑；
4. 混合参考：只有平台明确支持并能区分多参考职责时才使用。
