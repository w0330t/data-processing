import datetime
import pandas as pd

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


def convert_timestamp(timestamp):
    """将时间戳转换为自然时间

    Args:
        timestamp (int): 毫秒级别的时间戳

    Returns:
        datetime: 自然时间
    """
    return datetime.datetime.fromtimestamp(timestamp / 1000)