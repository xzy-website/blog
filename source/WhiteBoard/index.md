---
date: '2026-02-13T17:15:41.936433+08:00'
title: WhiteBoard
updated: '2026-02-13T17:15:41.738+08:00'
---
<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>极简白板 · 胶囊悬浮</title>
    <!-- Font Awesome 6 免费图标库，仅用于工具图标，轻量干净 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* 彻底全屏，无多余边距，隐藏滚动条 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: none; /* 防止拖动时选中文本 */
        }
body, html {
width: 100%;
height: 100%;
overflow: hidden;   /* 隐藏滚动条，纯白板 */
background: white;
}

/* 画布绝对底层，全屏 */
#canvas {
position: fixed;
top: 0;
left: 0;
width: 100vw;
height: 100vh;
display: block;
cursor: crosshair;  /* 默认绘图光标，移动工具会动态更改 */
background-color: white; /* 保证背景纯白，橡皮擦绘制白色覆盖 */
}

/* -------------------- 左侧胶囊工具栏 -------------------- */
/* 极小悬浮胶囊，完全贴合左侧，半透磨砂效果，无任何文字提示，只有图标 */
.toolbar-capsule {
position: fixed;
left: 20px;
top: 50%;
transform: translateY(-50%);
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
gap: 12px;          /* 按钮间距小，紧凑 */
padding: 14px 8px;  /* 上下内收，短胶囊 */
background: rgba(20, 20, 25, 0.65); /* 深色半透明背景 */
backdrop-filter: blur(8px);         /* 悬浮玻璃效果 */
-webkit-backdrop-filter: blur(8px);
border-radius: 40px; /* 胶囊大圆角 */
box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15); /* 轻柔阴影，悬浮感 */
border: 0.5px solid rgba(255, 255, 255, 0.2);
z-index: 100;
}

/* 每个工具按钮 —— 小而美的圆形，纯色功能 */
.tool-btn {
width: 44px;        /* 短小精致 */
height: 44px;
border-radius: 50%;
border: none;
background: rgba(30, 30, 35, 0.9); /* 默认深色底，但颜色笔会覆盖 */
display: flex;
align-items: center;
justify-content: center;
font-size: 20px;    /* 图标大小适中 */
color: white;
cursor: pointer;
transition: all 0.15s ease;
box-shadow: 0 2px 6px rgba(0,0,0,0.2);
position: relative;
}

/* 黑、红、蓝三支笔 —— 背景色即其颜色，直观无文字 */
.tool-btn[data-color="black"] {
background: #000000;
}
.tool-btn[data-color="red"] {
background: #e03a3a; /* 鲜明红色 */
}
.tool-btn[data-color="blue"] {
background: #2a6df4; /* 明亮蓝色 */
}
/* 橡皮擦与移动 —— 保持深灰，图标辨识 */
.tool-btn[data-tool="eraser"] {
background: #4a4a52;
}
.tool-btn[data-tool="hand"] {
background: #4a4a52;
}

/* 悬浮效果：轻微放大，增加亮边 */
.tool-btn:hover {
transform: scale(1.12);
box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5);
transition: 0.1s;
}

/* 当前激活的工具 —— 发光白边，清晰指示 */
.tool-btn.active {
box-shadow: 0 0 0 3px white, 0 0 0 5px rgba(255,255,255,0.3);
transform: scale(1.05);
}

/* 所有图标统一白色，干净 */
.tool-btn i {
color: white;
filter: drop-shadow(0 1px 2px rgba(0,0,0,0.3));
}

/* 橡皮擦图标略调 */
.fa-eraser {
font-size: 19px;
}
/* 移动抓手 */
.fa-hand {
font-size: 21px;
}

/* 移除点击闪烁 */
.tool-btn:active {
transform: scale(0.98);
}

/* 无任何其他提示元素，纯粹画布+工具栏 */

</style>

</head>
<body>
    <!-- 全屏画布 —— 唯一的内容区域 -->
    <canvas id="canvas"></canvas>

<!-- 左侧胶囊工具栏 —— 仅黑、红、蓝、橡皮、移动，无文字，无多余 -->

<div class="toolbar-capsule">
    <!-- 黑色画笔，data-color 用于切换颜色 -->
    <button class="tool-btn active" id="tool-black" data-color="black" title=""> 
        <i class="fas fa-paint-brush"></i>
    </button>
    <!-- 红色画笔 -->
    <button class="tool-btn" id="tool-red" data-color="red" title="">
        <i class="fas fa-paint-brush"></i>
    </button>
    <!-- 蓝色画笔 -->
    <button class="tool-btn" id="tool-blue" data-color="blue" title="">
        <i class="fas fa-paint-brush"></i>
    </button>
    <!-- 橡皮擦 -->
    <button class="tool-btn" id="tool-eraser" data-tool="eraser" title="">
        <i class="fas fa-eraser"></i>
    </button>
    <!-- 移动画布（抓手/平移） -->
    <button class="tool-btn" id="tool-hand" data-tool="hand" title="">
        <i class="fas fa-hand"></i>
    </button>
</div>

<script>
    (function(){
        "use strict";

        // ---------- 画布与上下文 ----------
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        // ---------- 白板核心数据 ----------
        // 世界坐标系中的所有笔划（绝对坐标）
        let strokes = [];           

        // 当前正在绘制的笔划（未完成）
        let currentStroke = null;   

        // 画布偏移量（世界原点相对于视口左上角的偏移） —— 实现移动画布
        let offsetX = 0, offsetY = 0;

        // ---------- 工具状态 ----------
        // 当前激活的工具: 'black', 'red', 'blue', 'eraser', 'hand'
        let currentTool = 'black';   

        // 绘图状态与移动状态互斥
        let isDrawing = false;      // 是否正在绘制（笔/橡皮）
        let isPanning = false;     // 是否正在拖拽画布（移动工具）

        // 移动相关暂存变量
        let lastPanX = 0, lastPanY = 0; // 上次鼠标位置（client坐标），用于计算偏移增量

        // ---------- 笔刷设定 ----------
        const BRUSH_SIZE = 3.2;          // 黑/红/蓝 笔触粗细
        const ERASER_SIZE = 22;          // 橡皮擦大小 (粗一些，擦除明显)
        const ERASER_COLOR = '#ffffff';  // 白色橡皮，完美融合背景

        // ---------- 初始化画布尺寸（全屏）----------
        function resizeCanvas() {
            const w = window.innerWidth;
            const h = window.innerHeight;
            canvas.width = w;
            canvas.height = h;
            drawAll(); // 尺寸变化后重绘所有内容
        }
        window.addEventListener('resize', resizeCanvas);

        // ---------- 重绘整个世界：应用偏移，绘制所有笔划 ----------
        function drawAll() {
            // 清空画布并填充纯白背景（同时作为橡皮擦底色）
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 保存当前上下文状态，应用画布偏移（平移）
            ctx.save();
            ctx.translate(-offsetX, -offsetY); // 视口移动：世界坐标 -> 画布坐标

            // 设置线条渲染质量
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';

            // 1. 绘制所有已完成的笔划
            strokes.forEach(stroke => {
                drawStroke(stroke);
            });

            // 2. 如果存在未完成的当前笔划（正在绘制），也绘制出来
            if (currentStroke) {
                drawStroke(currentStroke);
            }

            ctx.restore();
        }

        // 绘制单个笔划（点集渲染，支持单点画圆）
        function drawStroke(stroke) {
            if (!stroke.points || stroke.points.length === 0) return;

            ctx.beginPath();
            ctx.strokeStyle = stroke.color;
            ctx.lineWidth = stroke.lineWidth;
            ctx.fillStyle = stroke.color;  // 用于单点绘制

            const points = stroke.points;

            // 如果只有一个点 —— 画实心圆表示点
            if (points.length === 1) {
                const p = points[0];
                ctx.beginPath();
                ctx.arc(p.x, p.y, stroke.lineWidth / 2, 0, 2 * Math.PI);
                ctx.fill();
                return;
            }

            // 多个点：绘制连续路径
            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i].x, points[i].y);
            }
            ctx.stroke();
        }

        // ---------- 辅助：根据当前工具获取颜色和线宽 ----------
        function getToolSettings(tool) {
            switch (tool) {
                case 'black': return { color: '#000000', lineWidth: BRUSH_SIZE };
                case 'red':   return { color: '#e03a3a', lineWidth: BRUSH_SIZE };
                case 'blue':  return { color: '#2a6df4', lineWidth: BRUSH_SIZE };
                case 'eraser':return { color: ERASER_COLOR, lineWidth: ERASER_SIZE };
                default:      return { color: '#000000', lineWidth: BRUSH_SIZE }; // hand不需要
            }
        }

        // ---------- 结束当前绘画（强制完成笔划）----------
        function finishCurrentStroke() {
            if (currentStroke) {
                // 只有至少一个点才保存（防止空点击）
                if (currentStroke.points.length > 0) {
                    strokes.push({ ...currentStroke }); // 存入永久数据
                }
                currentStroke = null;
                isDrawing = false;
            }
        }

        // ---------- 切换工具（同时处理未完成笔画、状态重置）----------
        function setActiveTool(toolId) {
            // 如果正在绘画，强制完成当前笔划
            if (isDrawing && currentStroke) {
                finishCurrentStroke();
            }
            // 如果正在拖拽画布，强制停止平移
            if (isPanning) {
                isPanning = false;
            }

            // 更新当前工具
            currentTool = toolId;

            // 更新工具栏UI激活状态
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            // 根据当前工具激活对应按钮
            if (toolId === 'black') document.getElementById('tool-black').classList.add('active');
            else if (toolId === 'red') document.getElementById('tool-red').classList.add('active');
            else if (toolId === 'blue') document.getElementById('tool-blue').classList.add('active');
            else if (toolId === 'eraser') document.getElementById('tool-eraser').classList.add('active');
            else if (toolId === 'hand') document.getElementById('tool-hand').classList.add('active');

            // 改变画布光标：移动工具用grab，绘图工具用crosshair
            if (toolId === 'hand') {
                canvas.style.cursor = 'grab';
            } else {
                canvas.style.cursor = 'crosshair';
            }
        }

        // ---------- 坐标转换：画布视口坐标 → 世界坐标（绝对）----------
        function viewportToWorld(viewportX, viewportY) {
            return {
                x: viewportX + offsetX,
                y: viewportY + offsetY
            };
        }

        // ---------- 鼠标/触摸事件监听：绘图 + 画布移动 ----------
        function handleMouseDown(e) {
            e.preventDefault(); // 禁止拖拽选中/默认行为
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;   // 若CSS缩放，但我们已经设置canvas像素=窗口，所以比例应为1
            const scaleY = canvas.height / rect.height;
            const canvasX = (e.clientX - rect.left) * scaleX;
            const canvasY = (e.clientY - rect.top) * scaleY;

            // ----- 移动工具（hand）：激活画布平移 -----
            if (currentTool === 'hand') {
                isPanning = true;
                isDrawing = false;
                // 记录起始点client坐标，用于计算delta
                lastPanX = e.clientX;
                lastPanY = e.clientY;
                canvas.style.cursor = 'grabbing';
                return;
            }

            // ----- 绘图工具（笔/橡皮）-----
            if (currentTool !== 'hand') {
                // 如果之前有未完成的笔划，先结束（一般不会有）
                if (currentStroke) finishCurrentStroke();

                // 将视口坐标转为世界坐标并存储
                const world = viewportToWorld(canvasX, canvasY);
                const settings = getToolSettings(currentTool);

                // 新建笔划
                currentStroke = {
                    color: settings.color,
                    lineWidth: settings.lineWidth,
                    points: [{ x: world.x, y: world.y }]
                };

                isDrawing = true;
                // 立即绘制当前点（drawAll会处理单点）
                drawAll();
            }
        }

        function handleMouseMove(e) {
            e.preventDefault();

            // 1. 处理画布拖拽移动 (pan)
            if (isPanning && currentTool === 'hand') {
                const deltaX = e.clientX - lastPanX;
                const deltaY = e.clientY - lastPanY;
                // 更新偏移量（视口移动）
                offsetX -= deltaX;   // 注意方向：鼠标向右拖，画布内容向右移动 -> 世界坐标相对左移 -> 偏移减小
                offsetY -= deltaY;
                // 限制偏移避免无限? 不限制，自由移动。
                lastPanX = e.clientX;
                lastPanY = e.clientY;
                drawAll(); // 重绘全部，应用新偏移
                return;
            }

            // 2. 绘图：只有当前工具不是hand且正在绘制时才添加点
            if (!isDrawing || currentTool === 'hand' || !currentStroke) return;

            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const canvasX = (e.clientX - rect.left) * scaleX;
            const canvasY = (e.clientY - rect.top) * scaleY;

            // 转为世界坐标
            const world = viewportToWorld(canvasX, canvasY);
            const lastPoint = currentStroke.points[currentStroke.points.length - 1];

            // 防止同一像素过度添加点（可加微小阈值，但保留更顺滑）
            const dx = world.x - lastPoint.x;
            const dy = world.y - lastPoint.y;
            if (Math.sqrt(dx*dx + dy*dy) < 0.6) return; // 距离太近忽略，提高性能

            // 添加点并重绘
            currentStroke.points.push({ x: world.x, y: world.y });
            drawAll();
        }

        function handleMouseUp(e) {
            e.preventDefault();

            // 结束画布拖拽
            if (isPanning && currentTool === 'hand') {
                isPanning = false;
                canvas.style.cursor = 'grab';
                return;
            }

            // 结束绘图
            if (isDrawing) {
                finishCurrentStroke(); // 将currentStroke存入strokes并清空
                drawAll(); // 重绘确保最终状态
            }
        }

        // 防止鼠标离开canvas后还保持按下状态 —— 全局监听mouseup
        window.addEventListener('mouseup', handleMouseUp);
        window.addEventListener('mousemove', handleMouseMove); // 全局移动保证不丢事件

        // canvas事件
        canvas.addEventListener('mousedown', handleMouseDown);
        // 注意：mouseMove已在window监听，可避免移出画布无法更新偏移；但canvas上也要监听以确保进入绘图
        canvas.addEventListener('mousemove', handleMouseMove);
        // 阻止contextmenu弹窗
        canvas.addEventListener('contextmenu', (e) => e.preventDefault());

        // ---------- 工具栏按钮点击切换（无任何多余提示）----------
        document.getElementById('tool-black').addEventListener('click', () => setActiveTool('black'));
        document.getElementById('tool-red').addEventListener('click', () => setActiveTool('red'));
        document.getElementById('tool-blue').addEventListener('click', () => setActiveTool('blue'));
        document.getElementById('tool-eraser').addEventListener('click', () => setActiveTool('eraser'));
        document.getElementById('tool-hand').addEventListener('click', () => setActiveTool('hand'));

        // ---------- 触摸事件（移动端基础兼容，保持白板可用）----------
        function handleTouchStart(e) {
            e.preventDefault();
            const touch = e.touches[0];
            const fakeEvent = { ...e, clientX: touch.clientX, clientY: touch.clientY, preventDefault: e.preventDefault };
            handleMouseDown(fakeEvent);
        }
        function handleTouchMove(e) {
            e.preventDefault();
            const touch = e.touches[0];
            const fakeEvent = { ...e, clientX: touch.clientX, clientY: touch.clientY, preventDefault: e.preventDefault };
            handleMouseMove(fakeEvent);
        }
        function handleTouchEnd(e) {
            e.preventDefault();
            handleMouseUp(e);
        }
        canvas.addEventListener('touchstart', handleTouchStart);
        canvas.addEventListener('touchmove', handleTouchMove);
        canvas.addEventListener('touchend', handleTouchEnd);
        canvas.addEventListener('touchcancel', handleTouchEnd);

        // ---------- 初始化 ----------
        function init() {
            resizeCanvas();
            // 默认激活黑色画笔（已在HTML里有一个active类，但同步状态）
            setActiveTool('black');
            // 清空可能存在的演示笔画（无）
            strokes = [];
            drawAll();
        }

        init();
    })();
</script>

</body>
</html>

