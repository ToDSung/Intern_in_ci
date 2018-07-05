
# coding: utf-8

# In[2]:


import logging
import datetime
'''
log_filename = datetime.datetime.now().strftime("%Y-%m.log")
logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M:%S')
'''
def get_my_logger():
# 定義 handler 輸出 sys.stderr
# handler對象負責發送相關的信息到指定目的地。
    logger = logging.getLogger('')
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)

        # 設定輸出格式
        formatter = logging.Formatter('[%(asctime)s][line:%(lineno)d]function：%(funcName)s：%(message)s'
                                      ,datefmt='%H:%M:%S')
        # handler 設定輸出格式
        console.setFormatter(formatter)
        # 加入 hander 到 root logger

        logger.addHandler(console)
    return logger

logger = get_my_logger()

logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('critical')

