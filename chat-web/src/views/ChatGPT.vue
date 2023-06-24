<template>
    <div class="container" ref="messageList">
        <div v-for="(message, index) in messages" :key="index" class="messages">
            <div :class="message.role === 'USER' ? 'msg_bg' : 'msg'" v-text="message.role + '&nbsp;:&nbsp;&nbsp;' + message.content"></div>
        </div>
    </div>
    <div class="input-box">
        <input type="text" v-model="inputText" placeholder="请输入消息" @keyup.enter="sendMessage" />
        <button @click="sendMessage" :disabled="chatting">发送</button>
    </div>
</template>

<script>
import { io } from 'socket.io-client';
export default {
    data() {
        return {
            messages: [
                {content:'快来和我聊天吧', role: 'ChatGPT'}
            ],
            inputText: '',
            chatting: false,
            ws: null
        }
    },
    beforeDestroy(){
        this.ws.disconnect();
    },
    mounted() {
        // socket.io
        this.ws = io.connect(BASE_URL + '/chat', {
            query: 'user_id=' + Math.floor(Math.random()*10000) + 1
        })
        this.ws.on('connect', () => {
            console.log('WebSocket连接成功');
        });
        this.ws.on('message', (data) => {
            if (data === '$$over$$') {
                this.chatting = false;
            } else {
                let length = this.messages.length;
                let content = this.messages[length-1].content.concat(data);
                this.messages[length-1].content = content;
            }
            this.scrollToBottom();
        });
        this.ws.on('disconnect', () => {
            console.log('WebSocket连接断开')
            let length = this.messages.length;
            let content = this.messages[length-1].content;
            if (content.length === 0) {
                content = '抱歉，服务器发生异常了.'
                this.messages[length-1].content = content;
            }
            this.chatting = false;
            this.scrollToBottom();
        })
    },
    methods: {
        sendMessage() {
            if (this.inputText && !this.chatting) {
                this.messages.push({content: this.inputText, role: 'USER'});
                let res = {content: '', role: 'ChatGPT'};
                this.messages.push(res);
                this.scrollToBottom();
                this.chatting = true;
                this.ws.send(this.inputText);
                this.inputText = '';
            }
        },
        scrollToBottom() {
            this.$nextTick( () => {
                const messageList = this.$refs.messageList;
                messageList.scrollTop = messageList.scrollHeight;
            });
        }
    }
}
</script>

<style>
.container {
    flex: 1;
    width: 100%;
    margin-top: 10px;
    margin-bottom: 15px;
    overflow: auto;
}

.messages {
    margin-top: 10px;
    padding-left: 10px;
    width: 98%;
}

.msg {
    display: inline-block;
    width: 100%;
    box-sizing: border-box;
    text-align: left;
    padding-right: 20px;
    word-wrap: break-word;
    white-space: pre-line;
}

.msg_bg {
    display: inline-block;
    width: 100%;
    box-sizing: border-box;
    text-align: left;
    padding-right: 20px;
    background-color: #6d06d1;
    word-wrap: break-word;
    color: #fff;
    white-space: pre-line;
}

.input-box {
    flex: 2;
    width: 100%;
    margin-bottom: 10px;
    max-height: 45px;
}

input {
    width: 80%;
    height: 40px;
    margin-left: 5px;
    padding: 5px;
    box-sizing: border-box;
    border: 1px solid #ccc;
}

button {
    width: 15%;
    height: 40px;
    background-color: #6d06d1;
    margin-left: 5px;
    border: none;
    cursor: pointer;
    color: #fff;
}
</style>