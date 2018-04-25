import os, subprocess, time
from yowsup.layers import YowLayer
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity

allowedPersons=['551188442211','551191121009']
ap = set(allowedPersons)


class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)


    def onTextMessage(self, messageProtocolEntity):
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
        if messageProtocolEntity.getFrom(False) in ap:
            if 'hi' in messageProtocolEntity.getBody():
                antwort = 'HI!'
                self.toLower(receipt)
                self.toLower(TextMessageProtocolEntity(antwort, to = messageProtocolEntity.getFrom()))
            elif 'test' in messageProtocolEntity.getBody():
                t=float(subprocess.check_output(["cat /root/yowsup/auto/teste/test.txt"], shell=True)[:-1])
                ts=str(t)
                antwort = 'This test is '+ts+'.'
                self.toLower(receipt)
                self.toLower(TextMessageProtocolEntity(antwort, to = messageProtocolEntity.getFrom()))
            else:
                antwort = 'I dont understood.'
                self.toLower(receipt)
                self.toLower(TextMessageProtocolEntity(antwort, to = messageProtocolEntity.getFrom()))
        else:
            antwort = 'You arent a valid sender.'
            self.toLower(receipt)
            self.toLower(TextMessageProtocolEntity(antwort, to = messageProtocolEntity.getFrom()))
