from moocxing.package import MOOCXING
from moocxing.robot.Brain import Brain

mx = MOOCXING()

APP_ID='23084370'
API_KEY='KpNbsHjl3BPsKGXgc6r9bbzt'
SECRET_KEY='RyqDNA3ACZB857kLxM7VHCGZxGk4HylB'

#初始化播放器和录音模块
media =mx.initMedia()
#初始化串口模块
serial = mx.initSerial( com="COM31" , bps=9600)
#初始化语音识别+语音合成模块
speech = mx.initSpeech( APP_ID,API_KEY,SECRET_KEY)

mc = mx.initMinecraft()
print("******************初始化完成******************\n" )

#初始化技能插件
brain =Brain( {"media" : media,
               " speech" : speech,
               "serial" : serial,
               "minecraft": mc})
print("***************技能插件加载完成***************\n")

#i语音合成十播放
def TTSPlay ( text):
    speech.TTS(text)
    media.play( )
    
#录音+语音识别
def recordSTT( ):
    media.record( )
    return speech.STT()


while True:
    result = recordSTT()

    if not brain.query(result, _print=True):
        if '左转' in result:
            TTSPlay('好的，左转')
            serial.send('tl$')
        if '右转' in result:
            TTSPlay('好的，右转')
            serial.send('tr$')
        if '前进' in result:
            TTSPlay('好的，前进')
            pos = mc.player.getTilePos()
            mc.player.setTilePos(pos.x + 1, pos.y, pos.z)
        if '后退' in result:
            TTSPlay('好的，后退')
            pos = mc.player.getTilePos()
            mc.player.setTilePos(pos.x - 1, pos.y, pos.z)
        if '左移' in result:
            TTSPlay('好的，左移')
            pos = mc.player.getTilePos()
            mc.player.setTilePos(pos.x, pos.y, pos.z - 1)
        if '右移' in result:
            TTSPlay('好的，右移')
            pos = mc.player.getTilePos()
            mc.player.setTilePos(pos.x, pos.y, pos.z + 1)
        if '约翰' in result:
            if '左转' in result:
                TTSPlay('好的，约翰左转')
                mc.player.setDirection()
                rotation = mc.player.getRotation()
                mc.player.setRotation(rotation - 30)
            elif '右转' in result:
                TTSPlay('好的，约翰右转')
                mc.player.setDirection()
                rotation = mc.player.getRotation()
                mc.player.setRotation(rotation + 30)
