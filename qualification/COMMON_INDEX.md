# 常见技术指标

## 大势型

### ABI(Absolute Breadth lndex)

    绝对广量指标

    ABI = abs(Advance - Decline) / sum(Advance, Decline)

    ABI较小说明市场中性，即处在平衡状态下，但当ABI过大，说明市场出现波动，比如上涨家数远大于下跌家数（反之亦然）则表明市场情绪变热（反之变恐慌）
    
### ADL(A·D·Line)

    腾落指标

    ADL = ∑(Advance - Decline)

    该指标与股市指数是同向，因为上涨和下跌过程中，一部分就体现在家数上，特别是在有涨跌幅限制的市场

### ADR(Advance Decline Ratio)

    涨跌数比率指标

    ADL = ∑(Advance) / ∑(Decline)

    同ADL指标一样，体现整个市场的情况，如果ADL过大，表现出超买的现象，如果ADL过小，则说明超卖，具体阈值根据市场判定

### ADV(Advance Decline Volume)

    涨跌交易量比

    ADV = ∑(Advance Volume) / ∑(Decline Volume)

    单独使用，只能体现当前市场的交易方向，当市场比较热的时候，则体现在ADV增大，说明买入成交量增多，但如果过大，则说明很可能出现超买现象，反之则是超卖

### ARMS(Arms Index)

    阿姆氏指标

    R = ADL / ADV

    ARMS = EMA(R, n)

    一个综合指标，进行N日平均的涨跌统计指标，可以作为反转指标，当ARMS < 1(即ADL < ADV)，说明成交量向下跌股流动，反之则是成交量向上涨股流动

### BTI(Breadth Thrust Index)

    广量指标

    BTI = Advance / sum(Advance, Decline)

    参考ABI

### C&A(China&America)

    钱龙中线指标

    ---待补充---

### COPPOCK(Coppock Curve)

    估波指标

    >wiki: The indicator is designed for use on a monthly time scale. It is the sum of a 14-month rate of change and 11-month rate of change, smoothed by a 10-period weighted moving average.  https://en.wikipedia.org/wiki/Coppock_curve

    属于中期买入指标，当市场长期处于上涨态势，利用该指标刨除短期下跌变动，说明整体处于上涨阶段，当指标大于0的时候，说明已经处于涨的状态

### MCL(McClellan Oscillator)

    麦克连指标

    Oscillator = EMA( Advance - Decline, 19) - EMA( Advance - Decline, 37)

    当指标大于0的时候，说明仍有上涨动力，当小于0，说明短期支撑力度不够，属于短中期指标，寻求趋势反转

### MSI(McClellan Summation Index)

    麦氏总合指标

    Index = Previous Index's Value + Current McClellan Oscillator Value 

    基于MCL衍生出的，弥补MCL的不足，是寻找一个长期趋势顶端的

### OBOS(Over Bought Over Sold)

    超买超卖线

    OBOS = EMA( Advance, n) - EMA( Decline, n)

    中期指标，若出现数值同符号，可理解为长期同向市场开始一段时间

### TRIX(triple-smoothed exponential moving average)

    三重指数平滑平均线
    
    1. Smooth prices (often closing prices) using an N-day exponential moving average (EMA).
    
    2. Smooth that series using another N-day EMA.
    
    3. Smooth a third time, using a further N-day EMA.
    
    4. Calculate the percentage difference between today's and yesterday's value in that final smoothed series.

    https://en.wikipedia.org/wiki/Trix_(technical_analysis)

    利用交叉线的方式提供信号指数，常用价格作为计算基础

### 



    

