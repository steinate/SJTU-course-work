from moocxing.package import MOOCXING
from moocxing.robot.Brain import Brain

mx = MOOCXING()

#自己注册百度API
APP_ID='23084370'
API_KEY='KpNbsHjl3BPsKGXgc6r9bbzt'
SECRET_KEY='RyqDNA3ACZB857kLxM7VHCGZxGk4HylB'

#初始化播放器和录音模块
media =mx.initMedia()
#初始化串口模块
serial = mx.initSerial( com="COM31" , bps=9600)
#初始化语音识别+语音合成模块
speech = mx.initSpeech( APP_ID,API_KEY,SECRET_KEY)
print("******************初始化完成******************\n" )

#初始化技能插件
brain =Brain( {"media" : media,
               " speech" : speech,
               "serial" : serial,})
print("***************技能插件加载完成***************\n")

#语音合成十播放
def TTSPlay ( text):
    speech.TTS(text)
    media.play( )
    
#录音+语音识别
def recordSTT( ):
    media.record( )
    return speech.STT()
    
while True:
    result =recordSTT()
    '''
    brain . query ( result,_print = False )
    参数:
        result:语言识别内容
        _print:是否打印识别内容
    返回:技能是否匹配成功(True/False )
    
    技能:查时间、查天气、听音乐
    查时间关键词:时间、几点、口期、日子、几号、星期
    查天气关处词:天气〔要加城市)
    听音乐关健词:听、播放、首、歌+歌名
                 暂停、继续、停止
                (网易云API部分歌曲可能不版权)
    '''
    if not brain.query( result,_print=True ):
        if "左转"in result:
            TTSPlay ("好的,向左转")
            serial.send( " 1a2a" )
        if "右转"in result:
            TTSPlay ("好的，向右转")
            serial.send( "3a4a" )
