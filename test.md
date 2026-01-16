## 2. 复分析例题五 (Example 5 of Complex Analysis)

*   **推导思想：** 本题核心目标是计算实积分 $\int_{-\infty}^{\infty} \frac{\cos x}{x^2 + 1}  dx$。与简单回归的 OLS 推导逻辑类似——OLS 是最小化残差平方和，本题则是利用**复变函数留数定理**，将实轴上的无穷积分转化为复平面上的闭合回路积分，通过求解极点留数、验证大弧积分收敛性，最终取实部得到结果。
    *   构造辅助复变函数：选取 $f(z) = \frac{e^{iz}}{z^2 + 1}$（利用欧拉公式 $e^{iz} = \cos z + i\sin z$，其实部恰好是目标积分的被积函数 $\frac{\cos x}{x^2 + 1}$）。
    *   确定积分路径：选择上半平面闭合回路（包含实轴区间 $[-R, R]$ 和上半圆周 $C_R$），令 $R \to \infty$，仅包含上半平面的极点以简化计算。

***
**积分求解步骤 (Steps of Integral Solution)：**

*   **步骤1：寻找极点**：令分母 $z^2 + 1 = 0$，解得极点为 $z = i$ 和 $z = -i$。其中仅 $z = i$ 位于上半平面，因此只需计算该极点处的留数。
*   **步骤2：计算极点留数**：根据一阶极点留数公式，
    $$
    \operatorname{Res}(f, i) = \lim_{z \to i} (z - i) \frac{e^{iz}}{(z - i)(z + i)} = \frac{e^{i \cdot i}}{2i} = \frac{e^{-1}}{2i}.
    $$
*   **步骤3：应用留数定理**：闭合回路积分等于 $2\pi i$ 乘以回路内所有极点的留数之和，因此
    $$
    \oint_{C} f(z)  dz = 2\pi i \cdot \operatorname{Res}(f, i) = 2\pi i \cdot \frac{e^{-1}}{2i} = \pi e^{-1}.
    $$
*   **步骤4：验证大弧积分收敛到 0**：当 $R \to \infty$ 时，上半圆周 $C_R$ 上的积分 $\int_{C_R} f(z)  dz \to 0$（由 Jordan 引理，因 $|f(z)| \leq \frac{1}{R^2 - 1}$，且 $\left|\int_{C_R} f(z)  dz\right| \leq \pi R \cdot \frac{1}{R^2 - 1} \to 0$）。
*   **步骤5：拆分积分并取实部**：闭合回路积分可拆分为实轴积分与大弧积分之和：
    $$
    \int_{-\infty}^{\infty} \frac{e^{ix}}{x^2 + 1}  dx + \int_{C_R} f(z)  dz = \pi e^{-1}.
    $$
    令 $R \to \infty$，大弧积分消失，对左侧实轴积分取实部（右侧为实数）：
    $$
    \int_{-\infty}^{\infty} \frac{\cos x}{x^2 + 1}  dx = \operatorname{Re}\left( \pi e^{-1} \right) = \frac{\pi}{e}.
    $$

***
**例题结论与性质 (Conclusion and Properties)：**

*   **核心结论**：最终求得目标积分结果为 $\int_{-\infty}^{\infty} \frac{\cos x}{x^2 + 1}  dx = \frac{\pi}{e}$，即原题初始形式 $-\int_{-\infty}^{\infty} \frac{\cos x}{x^2 + 1}  dx = -\frac{\pi}{e}$。
*   **方法性质**：该方法（留数定理求解实无穷积分）具备类似 OLS 的优良性质：
    *   **有效性 (Efficiency)**：相较于实分析方法（如傅里叶变换），留数定理直接通过极点特征求解，计算步骤更简洁、误差更小。
    *   **一致性 (Consistency)**：随着积分区间 $R$ 趋近于无穷大，估计值（积分结果）收敛到真实值 $\frac{\pi}{e}$。
    *   **通用性 (Generality)**：该方法可推广到形如 $\int_{-\infty}^{\infty} \frac{\cos ax}{x^2 + b^2}  dx$ 的一类积分，类似 OLS 可推广到多元线性回归。