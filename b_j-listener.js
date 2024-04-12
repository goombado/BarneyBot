#!/usr/bin/env node
const ArgumentParser = require('argparse').ArgumentParser;
const parser = new ArgumentParser({
    version: '6.9.420',
    addHelp:true,
    description: 'Barney Voice Channel Listener: Baby Bop',
});
parser.addArgument(
    [ '-c', '--channel' ],
    {
        help: 'voice channel id',
    },
);
parser.addArgument(
    [ '-u', '--user' ],
    {
        help: 'user id',
    },
);
const args = parser.parseArgs();
console.dir(args);
console.log(`Voice Channel ID: ${args.channel}`);

const Discord = require('discord.js');
const client = new Discord.Client();
const fs = require('fs');
const { OpusEncoder } = require('@discordjs/opus');
const { Buffer } = require('buffer');
const encoder = new OpusEncoder(48000, 2);

const snooze = ms => new Promise(resolve => setTimeout(resolve, ms));
const sleep = async () => {
  await snooze(15000);
};

async function bufpush(stream) {
    const buffers = [];
    stream.on('data', function(data) {
        buffers.push(data);
    });
    await sleep();
    return buffers;
}

client.once('ready', async () => {
    let i = 1;
    const writing = true;
    console.log('Ready!');
    const channel = client.channels.cache.get(args.channel);
    const connection = await channel.join()
    .catch(err => console.error(err));
    const audio = connection.receiver.createStream(args.user, { mode: 'pcm', end: 'manual' });
    while (writing) {
        const buffers = await bufpush(audio);
        const buf = Buffer.concat(buffers);
        fs.writeFile(`user_audio_recordings/${args.user}/recordings/${args.user}_${i.toString()}`, buf, function(err) {
            if (err) throw err;
            console.log(`Stream ${i.toString()} written`);
        });
        // audio.pipe(fs.createWriteStream(`${args.user}_${i.toString()}`));
        fs.writeFile(`user_audio_recordings/${args.user}/completed/completed_${i.toString()}`, '.', function(err) {
            if (err) throw err;
            console.log(`Stream ${i.toString()} completed`);
        });
        i++;
    }
});
client.login('definitely not secret');