import discord
import threading
import asyncio
import time, math, random
import sounddevice as sd #from https://python-sounddevice.readthedocs.io/en/0.3.14/

# Gets audio from the microphone
class MicrophoneAudioSource(discord.PCMAudio):
    def __init__(self,  duration_ms=20):
        self.SAMP_RATE_HZ = 48000.0 #48 KHz
        self.SAMP_PERIOD_SEC = 1.0/self.SAMP_RATE_HZ
        self.NUM_SAMPLES = int((duration_ms/1000.0)/self.SAMP_PERIOD_SEC)
        self.audioStream = sd.RawInputStream(samplerate=self.SAMP_RATE_HZ, channels=2, dtype='int16', blocksize=self.NUM_SAMPLES)
        self.audioStream.start()


    def read(self):
        retVal = self.audioStream.read(self.NUM_SAMPLES)
        rawData = bytes(retVal[0])
        return rawData
        
        


# Actual discord API. This is what does the heavy lifting
class CasseroleDiscordBotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.audioSource = TestAudioSource()
        self.mikeAudioSource = MicrophoneAudioSource()
        self.voiceClient = None

        #Inputs from the outside world - changing these will change the Client state
        self.connectRequest = False
        self.shutdownRequest = False
        
        self.isLoggedIn= False
        self.isConnected= False
        self.connectRequestPrev = False

        # Trigger a periodic loop to update the Client state based on outside inputs
        self.loop.create_task(self.periodicStateCheck())

    # Initiates the Audio Connection
    async def voiceConnect(self):
        if(self.voiceClient == None):
            channel = discord.utils.get(client.get_all_channels(), name='General')
            self.voiceClient = await channel.connect()
            self.voiceClient.play(self.mikeAudioSource)
            self.isConnected = True

    # Ends the Audio Connection
    async def hangUp(self):
        if(self.voiceClient is not None):
            await self.voiceClient.disconnect()
            self.voiceClient = None
            self.isConnected = False

    # Hook to capture Discord Login Event
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.isLoggedIn = True

    # Hook to process incoming text
    async def on_message(self, message):
        if message.author == self.user:
            return
          
        # Handle phone commands
        if message.content.startswith('$callin'):
            print("Connect Command from {}".format(message.author))
            await self.voiceConnect()

        if message.content.startswith('$hangup'):
            print("Disconnect Command from {}".format(message.author))
            await self.hangUp()


    # Main periodic loop 
    async def periodicStateCheck(self):
        while(True):
            if(self.isLoggedIn):        
                #Only run updates if we're connected

                #Check if connection request has changed
                if(self.connectRequest != self.connectRequestPrev):
                    #Call or hang up as needed
                    if(self.connectRequest):
                        print("Connecting to Voice")
                        await self.voiceConnect()
                    else:
                        print("Hanging Up from Voice")
                        await self.hangUp()
                    self.connectRequestPrev = self.connectRequest

                # Update the string representing the curretly-speaking user
                if(self.connectRequest == True ):
                    member = self.guilds[0].get_member(self.audioSink.curSpeakerID)
                    if(member is not None):
                        if member.nick is not None:
                            self.speakingUserString = str(member.nick)
                        else:
                            self.speakingUserString = str(member)
                else:
                    self.speakingUserString = "..."

                # Check if we're supposed to shut down.
                if(self.shutdownRequest == True):
                    print("Shutting Down...")
                    await self.shutDown()
                    return

            # Allow other stuff to run
            await asyncio.sleep(0.25)


    async def shutDown(self):
        await self.logout()


#############################################
## Main code execution starts here
if __name__ == "__main__":
    client = CasseroleDiscordBotClient()
    print("Connecting to Discord...")
    client.run('whats a token')