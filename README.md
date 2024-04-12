# BarneyBot - the world's worst Discord bot

BarneyBot is/was a Discord Bot that I cobbled together over the course of my final year of high school. I haven't tried running it in a long time, and I'm 100% certain that changes to the Discord Bot API mean that, in its current state, it will not function. I don't care about him enough to resurrect him, but I want his legacy to live on. Thank you Barney for all you have done. May you and your spaghetti code live on in this public GitHub repo, and may any private keys I've accidentally left in your files be scraped by bots for years to come.

<a name="toc"/>

<style>h1,h2,h3,h4 { border-bottom: 0; } </style>

## Table of Contents  

[What I learnt - a TL;DR](#tldr)

[Features](#features)

-   [Word Counter](#wordcount)
-   [Word Identifier](#wordidentif)
    -   [Word Identification is hard](#wordhard)
    -   [Coupons](#coupon)
-   [Mafia](#mafia)
-   [Soundboard](#soundboard)
-   [Equation Grapher](#eqn)
-   [School](#school)
-   [Valorant](#valorant)
-   [Speech to Text](#stt)
-   [Integral Generator and Solver](#integration)

[Caveats](#caveats)

-   [Exclusivity](#exclusive)
-   [Scalability](#scalability)

[Installation](#installation)

[License](#license)

<a name="tldr"/>

## What I learnt - a TL;DR

I made Barney almost with the sole purpose to get better at Python and Programming. I did lots of research and learnt many concepts on the fly, often after a consequence of not having implemented said concept. As a quick list of things this taught me:

Regex; Advanced filtering and character identification; OCR; Image manipulation; Permissions, ownership and inheritence; Event handling and listeners; OAuth 2.0; API usage; Game design(?); Speech-to-text recognition and how hard it is; JavaScript and Promises; Pagification and information presentability

<a name="features"/>

## Features

From memory, BarneyBot has the following features.

<a name="wordcount"/>

### Word Counter

Given a regex pattern for certain words, Barney will make a count of each time any of those words are said, and keep track of this in a leaderboard. I used this as a swear-word detector, but this involved writing out the swear words I wanted to identify in Barney's code. In ensuring this monument stays tasteful, I have removed the specific pattern used.

<a name="wordidentif"/>

### Word Identification

About half of Barney's code was dedicated to the in-joke of removing any user who wrote the word "kpop". This was an arbitrary choice, and kpop music is great, but it made my friends mad which is obviously funny so I guess that's the word I chose. The idea was originally to see if any message had this word, and kick any user who typed it out. Barney would reach out to the user via Direct Message for the user to apologise, and if an apology was received within one minute, they would receive an invite back.

<a name="wordhard"/>

#### Word Identification is hard

Turns out this is really really hard. What I thought would be a simple feature became a never-ending game of cat and mouse attempting to stop any way of users posting this word. A capital "i" and a "less than" symbol, when put together, look like a capital K - "I<", and so this and similar work-arounds had to be stopped. I implemented checks against zero-width spaces. I utilised the Unicode "confusables.txt", a text file containing unicode characters that look similar to english letters and are often used to bypass letter-detection filters. I learnt how to use basic OCR so that (some) images with the word "kpop" would be treated in the same way. If a user wrote the word while Barney was offline, it would still be there, so on each message Barney would read the last 30 messages sent, and kick any user where a match was found.

The code is **brutally** inefficient, but it worked. People who wrote a phrase like the colloquial "ok pop off" (in reference to someone doing well) would not be kicked, even though "k pop" was detected. Navigating all of these edge cases was difficult, but a great lesson in pen-testing my own code to ensure maximum function and usability although at the cost of any semblance of efficiency. I'm pretty sure each check was O($n^4$​​) or something ridiculous.

<a name="coupon"/>

#### Coupons for word-identification grace periods

At my whim, I could generate "coupons" for users to gain a grace period for being kicked for typing the trigger word. Each coupon would come with a one-time user QR code, encoding a random string stored by Barney in another text file. When a user would send this QR code, provided it had not been used before, Barney would "redeem" the coupon and the user would gain immunity from being kicked by saying the trigger word. Coupons could be generated for 1, 3 or 7 days. This involved generating QR codes, layering them onto an image template, and then reading any QR codes sent by users and checking for a match.

<a name="mafia"/>

### Mafia

A very basic form of Mafia was implemented. It never truly worked, as lots of edge cases broke the program, but at its core it worked. Private Discord roles would be distributed randomly, secret text and voice channels would be created only accessible to mafia, and messages would be used to vote. I swear I played one game where no one broke anything and it was really fun.

<a name="soundboard"/>

### Soundboard

This is the feature I am proudest of. Discord now has a soundboard feature which kind of sucks for Barney, but I like to think they shamelessly stole the idea from my private code repository. I didn't really understand permissions or ownership at the time, or how to correctly implement them, but that did not stop me. I'm pretty proud of this one, as the ownership actually worked. The idea was anybody could upload a sound file to Barney privately, along with a list of commands to trigger that sound effect. After this, while in a voice channel, you can type in any of these commands, and Barney will join the voice channel and play the audio file. There is a global cooldown to stop users from abusing this feature.

You could upload a voice file with a command used by a previous one, uploaded by any user. In this case, Barney will randomly select a file to play. A user can delete a command, however this will delete associations that command has only with files that user owns. The same goes for the audio files themselves, as they can only be removed by the user that uploaded them. The ownership implementation was very clunky, and information was store across I think three text files, but it worked very well. Some examples are included here.

<a name="eqn"/>

### Equation Grapher

If a user typed in a message with an equation that could be graphed, Barney would try to do so using Desmos' API. It would try to calculate any asymptotes the graph had, as well as the derivative, double derivative and their respective asymptotes. The idea was to use it as a helper for people doing Maths (me) and who would have trouble calculating and visualing these values and equations (also me). It would spit it out on a very poorly formatted, CSS-less HTML document, but I was pretty proud of this feature.

<a name="school"/>

### School

During COVID, we had high school at home. I gave Barney a bunch of features for keeping track of school times and simulating what trains people would normally get on to go home. My favourite feature, however, was utilising the API of our School assignment/subject system, Schoology, to display upcoming assignment information, as it was impossible on the website itself to distinguish between assignments, regular periods, and unassessed work. This was, in retrospect, probably the only conventionally "useful" feature Barney had, and was good introduction into OAuth and API usage/permissions.

<a name="valorant"/>

### Valorant Store Checker

The final feature added to Barney about two years ago. My friends were into playing the video game Valorant, and would often check the store to see what skins were avilable for purchase. However, to do so you would have to open the game. Although Valorant has no official API, I found an API online that someone had implemented themselves to somehow get this store information. I created a tool for poeple to check their Valorant stores. It used custom Discord embeds to generate this information in a presentable way. This is probably the best programmed feature of Barney, as I had 1.5 years of University coding under my belt before implementing this.

Ensures that users are only able to access their own personalised Valorant store by having them log in privately via DM. Has support for two factor authentication, and stores encrypted login details. Caches the store if unchanged for users, until new store items are available. Presents the store with images pulled from public Valorant asset APIs, so that users can see exactly what is available to purchase.

Currently broken as the API I used to get store info is no longer publicly accessible.

<a name="stt"/>

### Unused - Speech to Text

I really tried hard to get this to work. This feature was an experimental feature of Discord.js, the JavaScript counterpart of Discord.py. The idea was utilising a (borderline unusable) feature of discord.js that allowed it to save the audio it heard in chunks. This could then be used for audio processing, such as identifying user voice commands, and add to Barney's functionality. It required a separate bot, as one bot could not be run on both discord.js and discord.py, but I was up for the challenge.

I never got this to work fully, and by the time I was really trying my hardest to get it to work, the HSC was rolling around and so I had to give it a rest. This is the only part of Barney that I would really like to come back to, as it's the only part still left unresolved in my head. I got as far as it actually listening to my voice and saving a recording of my voice, but that was about it. Recognition needed a bit more work, but I almost got there.

<a name="integration"/>

### Unused - Integration question and worked solution generator

This ended up becoming an idea to make this separate from Barney, but the remnants of all the work I did are still here. The idea was to utilise the python library SymPy, and specifically a feature it had called "ManualIntegrate". This would give you the integral of an equation you would give it, but rather than using advanced efficient techniques, it would attempt to solve it using "by-hand" techniques. It would give the solution as a tuple of methods, each of which may have sub-methods applied to sub-equations. Once this is generated, you could interpret each of these steps and display it in a user-friendly way, with equation formatting, to generate worked solutions for an integral. If randomness were applied to equation inputs, this could in theory generate, and solve, integrals using by hand methods and create worked solutions on the fly. Parameters could be input to test only specific methods, and solutions would be created. I was really excited by this.

I wanted this to be a way to practice high-school level integration, as the bank of questions we could use to practice was quite scarce. I got as far as outputting some of the output into LaTeX, but was learning about Object-Oriented Programming, LaTeX, CSS and SymPy all at the same time. I bit off a bit more than I could chew at the time, and never had the time to finish it. I would go back to this, but the rise of AI tools and the sophistication behind this generation makes me think this tool might be redundant. Maybe not.



<a name="caveats"/>

## Caveats

<a name="exclusive"/>

### Server Exclusivity

BarneyBot has lots of features, but lots of these are personalised to my high school friends. Our Discord Server ID is hard-coded into Barney's code, and Barney has essentially been designed spefically function only on this server. Many specific text channel and voice channel IDs are included. This is probably bad, but the server is not in use anymore so it should not be an issue. Don't expect to be able to use BarneyBot on any server that isn't this one specific server.

<a name="scalability"/>

### Scalability

Similar point to the last, but a point more on Barney's design philosophy. When I first started work on BarneyBot, I had just finished a ten day summer school whose aim was to teach high school kids how to code. I had no prior Python experience, and whilst my knowledge definitely increased, the shere volume of it was something that needed time to sit. I, in my infinite wisdom, did not give it this time, and went straight into making a project.

As an example, I only realised the practicality of functions about half way through the project. For a while, 95% of BarneyBot was an un-navigatable if-else block, testing for specific words that the user would write. Some of this was turned into functions, but as of writing I believe ~50% of Barney is one big function. About 1500 lines. Yippee.

This is all to say that it is impossible to know what Barney is doing at any given time. I don't remember. There is no way to know. I remember vague features, but that's about it. This was an incredibly valuable avenue for me to improve my programming ability, and I learnt so much from this, but it is not functional or scalable. I'm treating this as a museum.



<a name="installation"/>

## Installation Guide

Don't. It won't work. There are too many weird requirements that I never kept track of, it will be a miracle if I could get to run this even on my machine now.

<a name="license"/>

## License

MIT License. Go nuts.