import datetime
import pandas as pd

from pyecharts.charts import Grid, Kline, Line, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

def read_kline_data(file_path:str) -> pd.DataFrame:
    """
    从给定的 JSON 文件中读取K线数据，并重命名列名为指定的名称

    Args:
        file_path(str):JSON 文件的路径

    Returns:
        DataFrame:一个包含重命名后的列名的 DataFrame 对象
    """
    # 读取 JSON 文件数据
    df = pd.read_json(file_path)

    # 重命名列名
    df = df.rename(columns={0: 'timestamp', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})

    # 添加自然时间列
    df['datetime'] = df['timestamp'].apply(convert_timestamp)

    # 返回 DataFrame 对象
    return df


def convert_timestamp(timestamp: int) -> datetime.datetime:
    """将时间戳转换为自然时间

    Args:
        timestamp (int): 毫秒级别的时间戳

    Returns:
        datetime.datetime: 转换后的日期时间对象
    """
    return datetime.datetime.fromtimestamp(timestamp / 1000)


def create_kline_chart(dataframe: pd.DataFrame) -> Kline:
    """
    创建K线图的图表对象。

    参数:
        dataframe (pd.DataFrame): 包含K线数据的输入DataFrame。

    返回:
        Kline: K线图的图表对象。
    """
    data = dataframe[["open", "close", "low", "high"]].values.tolist()
    x_axis = dataframe["datetime"].tolist()

    kline = (
        Kline(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
        .add_xaxis(xaxis_data=x_axis)
        .add_yaxis("K线图", data)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                type_="log",
                min_="dataMin",
                max_="dataMax",
            ),
            title_opts=opts.TitleOpts(title="K线图"),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=True,
                    xaxis_index=[0, 1],
                    type_="inside",
                    pos_top="85%",
                    range_start=98,
                    range_end=100,
                ),
            ],
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000"),
            ),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777"),
            ),
        )
    )

    return kline


def create_line_chart(dataframe: pd.DataFrame, columns: list, subplot: bool=True) -> Line:
    """
    创建折线图

    Args:
        dataframe (pd.DataFrame): 数据源DataFrame
        columns (list): 需要显示的列名列表
        subplot (bool, optional): 是否使用subplot方式展示，默认为True

    Returns:
        Line: 折线图实例
    """
    # 创建折线图对象
    line = (
        Line()
        .add_xaxis(xaxis_data=dataframe["datetime"].tolist())
    )

    # 使用列表形式添加多个指标数据
    for column_name in columns:
        if column_name in dataframe.columns:
            line.add_yaxis(
                series_name=column_name,
                y_axis=dataframe[column_name].tolist(),
                is_smooth=True,
                is_hover_animation=False,
                linestyle_opts=opts.LineStyleOpts(width=1, opacity=0.8),
                label_opts=opts.LabelOpts(is_show=False),
                is_symbol_show=False,
            )

    if subplot:
        # 设置x轴和y轴的配置
        line.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                grid_index=1,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                is_scale=True,
                split_number=2,
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )

    return line


def create_bar_chart(dataframe: pd.DataFrame, columns: list, subplot: bool=True) -> Bar:
    """
    创建柱状图

    Args:
        dataframe (pd.DataFrame): 数据源 DataFrame
        columns (list): 需要绘制的列名列表
        subplot (bool, optional): 是否创建子图，默认为 True

    Returns:
        Bar: 柱状图对象
    """
    # 创建柱状图对象
    bar = (
        Bar()
        .add_xaxis(xaxis_data=dataframe["datetime"].tolist())
    )

    for column_name in columns:
        if column_name in dataframe.columns:
            # 添加柱状图数据系列
            bar.add_yaxis(
                series_name=column_name,
                y_axis=dataframe[column_name].tolist(),
                # xaxis_index=1,
                # yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )

    if subplot:
        # 设置全局配置项
        bar.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                grid_index=1,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                is_scale=True,
                split_number=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )

    return bar