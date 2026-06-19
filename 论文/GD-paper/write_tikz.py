# -*- coding: utf-8 -*-
import os

content = r"""% system_architecture_tikz.tex
\begin{figure}[htbp]
  \centering
  \begin{tikzpicture}[
    font=\small,
    greenNode/.style={
      draw=teal!70!black, rounded corners=3pt, align=center,
      line width=0.5pt, minimum width=2.6cm, minimum height=0.9cm,
      fill=teal!6, text=black!85,
    },
    blueNode/.style={
      draw=blue!60!black, rounded corners=3pt, align=center,
      line width=0.5pt, minimum width=2.6cm, minimum height=0.9cm,
      fill=blue!5, text=black!85,
    },
    chipNode/.style={
      draw=blue!70!black, rounded corners=3pt, align=center,
      line width=0.7pt, minimum width=2.8cm, minimum height=1.0cm,
      fill=blue!8, text=black!90,
    },
    ioNode/.style={
      draw=green!60!black!70, rounded corners=2pt, align=center,
      line width=0.4pt, minimum width=2.0cm, minimum height=0.7cm,
      fill=green!5, text=black!75,
    },
    purpleNode/.style={
      draw=violet!60!black, rounded corners=3pt, align=center,
      line width=0.5pt, minimum width=2.6cm, minimum height=0.9cm,
      fill=violet!5, text=black!85,
    },
    domain/.style={
      draw, dashed, rounded corners=6pt, fill=#1, line width=0.4pt,
      inner sep=6pt,
    },
    energy/.style={
      -{Latex[length=2.2mm]}, thick, draw=teal!70!black, line width=1.0pt,
    },
    signal/.style={
      -{Latex[length=1.8mm]}, draw=blue!60!black, line width=0.5pt,
    },
    data/.style={
      -{Latex[length=1.8mm]}, draw=teal!60!black!60, line width=0.4pt,
    },
    wireless/.style={
      -{Latex[length=1.8mm]}, dashed, draw=violet!50!black, line width=0.4pt,
    },
    labelSmall/.style={font=\small},
  ]

  % ==================== Nodes ====================
  % Power domain
  \node[greenNode] (pv) at (0.2,3.8) {\textbf{光伏输入}\\(36\,V)};
  \node[greenNode] (power) at (3.4,3.8) {\textbf{三端口功率变换}\\(四绕组耦合电感)};
  \node[greenNode] (out) at (6.6,3.8) {\textbf{输出端/负载}\\(220\,V/50\,Hz)};
  \node[blueNode] (driver) at (3.4,5.2) {\textbf{隔离驱动\&保护}\\UCC21540\\OC\_FAULT};
  \node[blueNode] (sample) at (3.4,2.4) {\textbf{采样调理}\\V\_PV / I\_PV\\V\_OUT / I\_OUT\\TEMP};

  % Control domain
  \node[chipNode] (g553) at (0.0,0.0) {\textbf{GD32G553 主控制板}\\系统调度 / ADC / HRTIMER\\CAN / UART / 故障输入};
  \node[ioNode] (bat) at (0.0,-2.0) {\textbf{16S LFP 电池组}\\BAT (40--58.4\,V)};
  \node[chipNode] (bms) at (4.8,-1.5) {\textbf{GD32C113 BMS板}\\GD30BM2016 AFE\\单体采样 / 电流检测\\均衡 / FET / SOC};

  % Communication domain
  \node[purpleNode] (wifi) at (7.8,1.0) {\textbf{GD32VW553 无线模块}\\WiFi 通信\\数据转发 / 参数交互};
  \node[purpleNode] (app) at (10.2,1.0) {\textbf{上位机 / App}\\状态显示 / 模式切换\\故障告警 / 日志};

  % ==================== Background domains ====================
  \begin{scope}[on background layer]
    \node[domain={teal!4}, fit={(pv) (power) (out) (driver) (sample)}] (powerDomain) {};
    \node[domain={blue!3}, fit={(g553) (bms) (bat)}] (ctrlDomain) {};
    \node[domain={violet!3}, fit={(wifi) (app)}] (commDomain) {};
    \node[below right=0.05cm and 0.3cm of powerDomain.north west,
          font=\small\bfseries, text=teal!70!black] {功率域 (Power)};
    \node[below right=0.05cm and 0.3cm of ctrlDomain.north west,
          font=\small\bfseries, text=blue!60!black] {控制域 (Control)};
    \node[below right=0.05cm and 0.3cm of commDomain.north west,
          font=\small\bfseries, text=violet!60!black] {通信域 (Communication)};
  \end{scope}

  % ==================== Connections ====================
  % Energy flow
  \draw[energy] (pv.east) -- node[above, labelSmall, text=teal!70!black] {能量输入} (power.west);
  \draw[energy] (power.east) -- node[above, labelSmall, text=teal!70!black] {稳压输出} (out.west);
  \draw[energy] (driver.south) -- node[right, labelSmall, text=teal!70!black] {栅极驱动} (power.north);
  \draw[data] (power.south) -- node[right, labelSmall, text=black!45] {反馈} (sample.north);

  % Control signals
  \draw[signal] ([xshift=-0.5cm] g553.north) |- node[pos=0.3, left, labelSmall, text=blue!60!black] {PWM 驱动} (driver.west);
  \draw[signal] (sample.west) -- ++(-1.0,0) |- node[pos=0.7, below=0.05cm, labelSmall, text=blue!60!black] {ADC 反馈} ([xshift=0.6cm] g553.east);

  % BMS links
  \draw[data] ([xshift=0.3cm] bat.east) -- ++(1.5,0) |- node[pos=0.7, below, labelSmall, text=teal!60!black!60] {单体电压/电流/温度} (bms.west);
  \draw[data] ([xshift=-0.3cm] bms.north) |- node[pos=0.4, above, labelSmall, text=teal!60!black!60] {CAN FD 遥测/保护状态} ([xshift=0.6cm, yshift=-0.2cm] g553.south);

  % Wireless links
  \draw[data] ([xshift=0.5cm] g553.east) -| node[pos=0.4, above, labelSmall, text=teal!60!black!60] {UART 数据帧} (wifi.south);
  \draw[wireless] (wifi.east) -- node[above, labelSmall, text=violet!60!black] {WiFi} (app.west);
  \draw[wireless] (app.south) -- ++(0,-0.6) -| node[pos=0.3, below, labelSmall, text=violet!60!black] {配置/模式命令} ([yshift=-0.15cm] wifi.south);

  \end{tikzpicture}
  \caption{系统总体架构示意图（多MCU协同光储一体化数字电源系统）}
  \label{fig:system_architecture}
\end{figure}
"""

path = r'C:\Users\akaczz\Desktop\论文\GD-paper\sections\tikz_architecture.tex'
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Written %d bytes' % len(content))
