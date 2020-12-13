"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.console.console import outputLog
import json


class OpenchatBotReponseObject:

    @staticmethod
    def get_parameter(data, name, defaultValue=None):
        if name in data:
            return data[name]
        else:
            return defaultValue


class OpenChatBotMediaDefaultAction(OpenchatBotReponseObject):

    def __init__(self, actiontype, label, payload):
        self.actiontype = actiontype
        self.label = label
        self.payload = payload

    @staticmethod
    def parse(json_data):
        actiontype = OpenchatBotReponseObject.get_parameter(json_data, 'type', None)
        label = OpenchatBotReponseObject.get_parameter(json_data, 'label', None)
        payload = OpenchatBotReponseObject.get_parameter(json_data, 'payload', None)
        return OpenChatBotMediaDefaultAction(actiontype, label, payload)

    def to_aiml(self):
        if self.actiontype == 'web_url':
            aiml = "<link>"
            aiml += "<text>%s</text>" % self.label
            if self.payload is not None:
                aiml += "<url>%s</url>" % self.payload
            aiml += "</link>"
            return aiml

        outputLog(None, "Unknown Default Action type [%s]" % self.actiontype)
        return None
    
    def to_json(self):
        default_action = {}
        default_action['label'] = self.label
        default_action['payload'] = self.payload
        default_action['type'] = self.actiontype
        return default_action

class OpenChatBotMediaButton(OpenchatBotReponseObject):

    def __init__(self, actiontype, client, label, payload):
        self.actiontype = actiontype
        self.client = client
        self.label = label
        self.payload = payload

    @staticmethod
    def parse(json_data):
        actiontype = OpenchatBotReponseObject.get_parameter(json_data, 'type', None)
        client = OpenchatBotReponseObject.get_parameter(json_data, 'client', None)
        label = OpenchatBotReponseObject.get_parameter(json_data, 'label', None)
        payload = OpenchatBotReponseObject.get_parameter(json_data, 'payload', None)
        return OpenChatBotMediaButton(actiontype, client, label, payload)

    def to_aiml(self):
        if self.actiontype == 'web_url':
            aiml = "<button>"
            aiml += "<text>%s</text>" % self.label
            if self.payload is not None:
                aiml += "<url>%s</url>" % self.payload
            aiml += "</button>"
            return aiml

        outputLog(self, "Unknown Button type [%s]" % self.actiontype)
        return None

    def to_json(self):
        button = {}
        button['client'] = self.client
        button['label'] = self.label
        button['payload'] = self.payload
        button['type'] = self.actiontype
        return button

class OpenChatBotMedia(OpenchatBotReponseObject):

    def __init__(self, shortDesc, longDesc, title, mimeType, src, default_action, buttons):
        self.shortDesc = shortDesc
        self.longDesc = longDesc
        self.title = title
        self.mimeType = mimeType
        self.src = src
        self.default_action = default_action
        self.buttons = buttons

    @staticmethod
    def parse(json_data):
        shortDesc = OpenchatBotReponseObject.get_parameter(json_data, 'shortDesc', None)
        longDesc = OpenchatBotReponseObject.get_parameter(json_data, 'longDesc', None)
        title = OpenchatBotReponseObject.get_parameter(json_data, 'title', None)
        mimeType = OpenchatBotReponseObject.get_parameter(json_data, 'mimeType', None)
        src = OpenchatBotReponseObject.get_parameter(json_data, 'src', None)

        default_action = None
        if 'default_action' in json_data:
            default_action = OpenChatBotMediaDefaultAction.parse(json_data['default_action'])

        buttons = None
        if 'buttons' in json_data:
            buttons = [OpenChatBotMediaButton.parse(button) for button in json_data['buttons']]

        return OpenChatBotMedia(shortDesc, longDesc, title, mimeType, src, default_action, buttons)

    def to_aiml(self):
        aiml = "<card>"
        aiml += "<image>%s</image>" % self.src
        aiml += "<title>%s</title>" % self.shortDesc
        aiml += "<subtitle>%s</subtitle>" % self.longDesc
        for button in self.buttons:
            if button.actiontype == 'web_url':
                aiml += "<button>"
                aiml += "<text>%s</text>" % button.label
                if button.payload is not None:
                    aiml += "<url>%s</url>" % button.payload
                aiml += "</button>"
        aiml += "</card>"
        return aiml

    def to_json(self):
        media_json = {}
        media_json['longDesc'] = self.longDesc
        media_json['mimeType'] = self.mimeType
        media_json['shortDesc'] = self.shortDesc
        media_json['src'] = self.src
        media_json['title'] = self.title
        media_json['buttons'] = []
        for button in self.buttons:
            media_json['buttons'].append(button.to_json())
        media_json['default_action'] = self.default_action.to_json()
        return media_json


class OpenChatBotChannel(OpenchatBotReponseObject):

    def __init__(self, markup, messaging, sms, tts):
        self.markup = markup
        self.messaging = messaging
        self.sms = sms
        self.tts = tts

    @staticmethod
    def parse(json_data):
        markup = OpenchatBotReponseObject.get_parameter(json_data, 'markup', None)
        messaging = OpenchatBotReponseObject.get_parameter(json_data, 'messaging', None)
        sms = OpenchatBotReponseObject.get_parameter(json_data, 'sms', None)
        tts = OpenchatBotReponseObject.get_parameter(json_data, 'tts', None)
        return OpenChatBotChannel(markup, messaging, sms, tts)

    def to_aiml(self):
        aiml = ""
        return aiml

    def to_json(self):
        channel_json = {}
        channel_json['markup'] = self.markup
        channel_json['messaging'] = self.messaging
        channel_json['sms'] = self.sms
        channel_json['tts'] = self.tts #oho
        return channel_json


class OpenChatBotTTS(OpenchatBotReponseObject):

    def __init__(self, actiontype, payload):
        self.actiontype = actiontype
        self.payload = payload

    @staticmethod
    def parse(json_data):
        actiontype = OpenchatBotReponseObject.get_parameter(json_data, 'type', None)
        payload = OpenchatBotReponseObject.get_parameter(json_data, 'payload', None)
        return OpenChatBotTTS(actiontype, payload)

    def to_aiml(self):
        aiml = "<tts>"
        aiml += "<type>%s</type>" % self.actiontype
        aiml += self.payload
        aiml += "</tts>"
        return aiml

    def to_json(self):
        tts = {}
        tts['type'] = self.actiontype
        tts['payload'] = self.payload
        return tts

class OpenChatBotSuggestion(OpenchatBotReponseObject):

    def __init__(self, actiontype, label, payload):
        self.actiontype = actiontype
        self.label = label
        self.payload = payload

    @staticmethod
    def parse(json_data):
        actiontype = OpenchatBotReponseObject.get_parameter(json_data, 'type', None)
        label = OpenchatBotReponseObject.get_parameter(json_data, 'label', None)
        payload = OpenchatBotReponseObject.get_parameter(json_data, 'payload', None)
        return OpenChatBotSuggestion(actiontype, label, payload)

    def to_aiml(self):
        if self.actiontype == 'web_url':
            aiml = "<link>"
            aiml += "<text>%s</text>" % self.label
            if self.payload is not None:
                aiml += "<url>%s</url>" % self.payload
            aiml += "</link>"
            return aiml

        outputLog(None, "Unknown Suggestion type [%s]" % self.actiontype)
        # natural_language should triger a new bot query
        return None

    def to_json(self):
        suggestion_json = {}
        suggestion_json['label'] = self.label
        suggestion_json['payload'] = self.payload
        suggestion_json['type'] = self.actiontype
        return suggestion_json

class OpenChatBotResponse(OpenchatBotReponseObject):

    def __init__(self, query, userId, timestamp, text, channel, infoURL, media, suggestions, context):
        self.query = query
        self.userId = userId
        self.timestamp = timestamp
        self.text = text
        self.channel = channel
        self.infoURL = infoURL
        self.media = media
        self.suggestions = suggestions
        self.context = context

    @staticmethod
    def parse(json_data):
        query = OpenchatBotReponseObject.get_parameter(json_data, 'query', None)
        userId = OpenchatBotReponseObject.get_parameter(json_data, 'userId', None)
        timestamp = OpenchatBotReponseObject.get_parameter(json_data, 'timestamp', None)
        text = OpenchatBotReponseObject.get_parameter(json_data, 'text', None)
        infoURL = OpenchatBotReponseObject.get_parameter(json_data, 'infoURL', None)

        channel = {}
        if 'channel' in json_data:
            channel = OpenChatBotChannel.parse(json_data['channel'])

        media = []
        if 'media' in json_data:
            media = [OpenChatBotMedia.parse(mediax) for mediax in json_data['media']]

        suggestions = []
        if 'suggestions' in json_data:
            suggestions = [OpenChatBotSuggestion.parse(suggestionx) for suggestionx in json_data['suggestions']]

        contexts = []
        if 'context' in json_data:
            contexts = json_data['context'][:]

        return OpenChatBotResponse(query, userId, timestamp, text, channel, infoURL, media, suggestions, contexts)

    def to_aiml(self):
        aiml = ""

        if self.text is not None:
            aiml += self.text

        if self.channel is not None:
            aiml += " "
            aiml += self.channel.to_aiml()

        if self.media:
            for media in self.media:
                media_aiml = media.to_aiml()
                if media_aiml:
                    aiml += " "
                    aiml += media_aiml

        if self.suggestions:
            for suggestion in self.suggestions:
                sugg_aiml = suggestion.to_aiml()
                if sugg_aiml:
                    aiml += " "
                    aiml += sugg_aiml

        return aiml

    def to_json(self):
        json_response = {}

        if self.query is not None:
            json_response['query'] = self.query
        else:
            json_response['query'] = ""

        if self.userId is not None:
            json_response['userId'] = self.userId
        else:
            json_response['userId'] = ""

        if self.timestamp is not None:
            json_response['timestamp'] = self.timestamp
        else:
            json_response['timestamp'] = ""

        if self.text is not None:
            json_response['text'] = self.text
        else:
            json_response['text'] = ""

        if self.infoURL is not None:
            json_response['infoURL'] = self.infoURL
        else:
            json_response['infoURL'] = ""

        if self.channel:
            json_response['channel'] = self.channel.to_json()
        else:
            json_response['channel'] = {}

        if self.media:
            json_response['media'] = []
            for media in self.media:
                json_response['media'].append(media.to_json())
        
        if self.suggestions:
            json_response['suggestions'] = []
            for suggestion in self.suggestions:
                json_response['suggestions'].append(suggestion.to_json())

        return json_response

class OpenChatBotStatus(OpenchatBotReponseObject):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    @staticmethod
    def parse(json_data):
        code = OpenchatBotReponseObject.get_parameter(json_data, 'code', None)
        if code is None:
            return None
        message = OpenchatBotReponseObject.get_parameter(json_data, 'message', None)
        return OpenChatBotStatus(code, message)

    def to_json(self):
        status_json = {}
        status_json['code'] = self.code
        status_json['message'] = self.message
        return status_json


class OpenChatBotMeta(OpenchatBotReponseObject):

    def __init__(self, botName, botIcon, version, copyr, authors):
        self.botName = botName
        self.botIcon = botIcon
        self.version = version
        self.copyr = copyr
        self.authors = authors

    @staticmethod
    def parse(json_data):
        botName = OpenchatBotReponseObject.get_parameter(json_data, 'botName', None)
        botIcon = OpenchatBotReponseObject.get_parameter(json_data, 'botIcon', None)
        version = OpenchatBotReponseObject.get_parameter(json_data, 'version', None)
        copyr = OpenchatBotReponseObject.get_parameter(json_data, 'copyright', None)
        authors = OpenchatBotReponseObject.get_parameter(json_data, 'authors', None)
        return OpenChatBotMeta(botName, botIcon, version, copyr, authors)
    
    def to_json(self):
        meta_json = {}
        meta_json['botName'] = self.botName
        meta_json['botIcon'] = self.botIcon
        meta_json['version'] = self.version
        meta_json['copyright'] = self.copyr
        meta_json['authors'] = self.authors
        return meta_json

