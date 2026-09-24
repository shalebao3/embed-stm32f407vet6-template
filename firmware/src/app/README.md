# app：业务编排层（App）

项目业务流程、状态机、控制算法和模式编排放在这里。

命名规则：

- 文件：`app_<功能>.c/.h`
- 公开 API：`App_<Module>_...`

App 可以调用 driver、bsp 和 common；不要在这里堆 CMSIS 寄存器级初始化或板级引脚配置。
