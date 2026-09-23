# App：FOC 业务编排层

FOC 状态机、控制流程、模式切换以及算法编排放在这里。

推荐命名：`App_<功能>.c/.h`。

App 可以调用 Driver、Bsp 和 Common；不要在这里堆 CMSIS 寄存器级初始化或板级引脚配置。
