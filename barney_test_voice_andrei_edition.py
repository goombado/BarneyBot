import discord
import asyncio
import speech_recognition as sr
import traceback


TOKEN = 'excuse me why do you want my token'
WIT_AI_KEY = "lol"
discord.opus.load_opus('C:/Users/andre/documents/Barney Bot/libopus-0.x64.dll')
close_flag = False


# we need a sink for the listen function, so we just define our own
# extremely simple: just appends data to a byte array buffer
class BufSink(discord.reader.AudioSink):
	def __init__(self):
		# byte array to store stuff
		self.bytearr_buf = bytearray()
		# sample width, which is (bit_rate/8) * channels
		self.sample_width = 2
		# 48000Hz sampling rate
		# doubled, because speech_recognition needs mono and we've got stereo
		self.sample_rate = 96000
		# calculated bytes per second, sample_rate * sample_width
		# we need this to know what slices we can take from the buffer
		# would be 96000, but mono
		self.bytes_ps = 192000

	# just append data to the byte array
	def write(self, data):
		self.bytearr_buf += data.data

	# to prevent the buffer from getting immense, we just cut the part we've
	# just read from it, using the index calculated when we extracted the part
	def freshen(self, idx):
		self.bytearr_buf = self.bytearr_buf[idx:]


class Barney(discord.Client):
	# init variables
	def __init__(self):
		super().__init__()
		# buffer to hold info
		self.buffer = BufSink()

client = Barney()

async def poster(client, buffer, target_channel):
	print('started posting')
	global close_flag
	global post_thread
	# instantiate our recognizer object
	recog = sr.Recognizer()
	print('speech recog start')
	# we don't want the thread to end, so just loop forever
	while True:
		# useless to try anything if we don't have anything in the buffer
		# wait until we have enough data for a 5-second voice clip in the buffer
		if len(buffer.bytearr_buf) > 960000:
			print('buffer length > 960000')
			# get 5 seconds worth of data from the buffer
			idx = buffer.bytes_ps * 3
			slice = buffer.bytearr_buf[:idx]

			# if the slice isn't all 0s, create an AudioData instance with it,
			# needed by the speech_recognition lib
			print(any(slice))
			if any(slice):
				print('slice isn\'t all zeros')
				# trim leading zeroes, should be more accurate
				idx_strip = slice.index(next(filter(lambda x: x!=0, slice)))
				if idx_strip:
					print('idx_strip')
					buffer.freshen(idx_strip)
					slice = buffer.bytearr_buf[:idx]
				# create the AudioData object
				audio = sr.AudioData(bytes(slice), buffer.sample_rate,
					buffer.sample_width)
				print('audio created')

				with open("audio_file.wav", "wb") as new_file:
					new_file.write(audio.get_wav_data())
				# send the data to get recognized
				try:
					print('try loop initiated')
					msg = recog.recognize_wit(audio, WIT_AI_KEY)
					print('try complete')
				except Exception as e:
					print(e)
					traceback.print_exc()
				# except sr.UnknownValueError:
					print("ERROR: Couldn't understand.")
				#except sr.RequestError as e:
				#	print("ERROR: Could not request results from Wit.ai service; {0}".format(e))

				# if we send a msg with all 0s or something unintelligible,
				# we'll get a message, but it'll be empty
				if msg:
					print('msg exists')
					# send the message to the async routine
					asyncio.run_coroutine_threadsafe(target_channel.send(msg), client.loop)

			# cut the part we just read from the buffer
			buffer.freshen(idx)
			print('buffer freshened')

		# since it's an infinite loop, we need some way to break out, once the
		# program shuts down
		if close_flag:
			break

post_thread = None

@client.event
async def on_message(message):
	global post_thread
	if message.content.lower().startswith("$here"):
		if message.author.voice is None:
			await message.channel.send("Sorry, you're not in a voice channel.")
		else:
			if client.voice_clients:
				await message.channel.send(f"Got it, moving to voice channel {message.author.voice.channel.name} and directing output to {message.channel.name}.")
				await client.voice_clients[0].move_to(message.author.voice.channel)
				client.voice_clients[0].listen(discord.reader.UserFilter(client.buffer, message.author))
				if post_thread == None:
					post_thread = True
					client.bg_task = client.loop.create_task(poster(client, client.buffer, message.channel))
				print(client.voice_clients[0])
			else:
				await message.channel.send(f"Got it, moving to voice channel {message.author.voice.channel.name} and directing output to {message.channel.name}.")
				await message.author.voice.channel.connect()
				client.voice_clients[0].listen(discord.reader.UserFilter(client.buffer, message.author))
				if post_thread is None:
					post_thread = True
					client.bg_task = client.loop.create_task(poster(client, client.buffer, message.channel))
				print(client.voice_clients[0])






client.run(TOKEN)