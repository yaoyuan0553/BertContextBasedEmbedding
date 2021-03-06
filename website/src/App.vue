<template>
    <div id="app">
        <FileUploader ref="fileUploader"/>
        <button class="open-file-uploader" @click="$refs.fileUploader.toggleMenu()">blahblah</button>
        <h1>副词语义相似度计算器</h1>
        <div class="input-div">
            <DropdownInput ref="wordDi" class="word-di" title="词汇" placeholder="选择词汇" @keypress.enter.prevent/>
            <DropdownInput ref="categoryDi" class="category-di" title="类别" placeholder="选择类别"/>
            <InputBox ref="countIb" class="count-ib" title="显示数量"/>
            <ComputeButton ref="computeButton" class="compute-button"/>
        </div>
        <SimilarityRankingGraph ref="simRankGraph"/>
        <button @click="$refs.simRankGraph.chart.prevCategory()">Prev</button>
        <button @click="$refs.simRankGraph.chart.nextCategory()">Next</button>
    </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';
import ComputeButton from './components/ComputeButton.vue';
import DropdownInput from './components/DropdownInput.vue';
import SimilarityRankingGraph from './components/SimilarityRankingGraph.vue'
import InputBox from './components/InputBox.vue';
import FileUploader from './components/FileUploader.vue';

import MessageManager from '@/ts-components/MessageManager';
import * as Mdt from '@/ts-components/MessageDataTypes';
import { plainToClass } from 'class-transformer';


@Component({
    components: {
        ComputeButton,
        DropdownInput,
        SimilarityRankingGraph,
        InputBox,
        FileUploader
    },
})
export default class App extends Vue {
    public $refs!: {
        computeButton: ComputeButton,
        wordDi: DropdownInput,
        categoryDi: DropdownInput,
        countIb: InputBox,
        simRankGraph: SimilarityRankingGraph,
        fileUploader: FileUploader
    };

    infoReceived: boolean = false;

    messageManager: MessageManager | undefined;

    private updateOnMessage(xhr: XMLHttpRequest, ev?: Event) {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let data = JSON.parse(xhr.responseText);
            if (data.hasOwnProperty('info')) {
                const response = plainToClass(Mdt.WordCategoryInfoResponse, data);
                // @ts-ignore
                this.$refs.wordDi.update(response.info.words);
                // @ts-ignore
                this.$refs.categoryDi.update(response.info.categories, true);
                this.infoReceived = true;
            }
            else if (data.hasOwnProperty('sim_ranks')) {
                const response = plainToClass(Mdt.SimilarityRankResponse, data);
                let words: string[] = [];
                let sims: number[] = [];
                for (let cat in response.sim_ranks) {
                    const catSimRanks = response.sim_ranks[cat];
                    for (let i = catSimRanks.length-1; i >= 0; i--) {
                        words.push(catSimRanks[i].word);
                        sims.push(catSimRanks[i].similarityScore);
                    }
                }
                // @ts-ignore
                this.$refs.simRankGraph.chart.update(response.sim_ranks);
            }
            // @ts-ignore
            this.$refs.computeButton.reset();
            // @ts-ignore
            this.$refs.simRankGraph.chart.chart.hideLoading();
        }
    }

    private collectRequestData() : Mdt.WordSimilarityRequest | null
    {
        // @ts-ignore
        const word = this.$refs.wordDi.value();
        // @ts-ignore
        const cat = this.$refs.categoryDi.value();
        // @ts-ignore
        const n = this.$refs.countIb.value();

        if (word === "")
            return null;

        let ret = new Mdt.WordSimilarityRequest(word, cat, n);
        if (cat === '[自动]')
            ret.category = 'null';

        return ret;
    }

    public created() {
    }

    private sendInfoRequest()
    {
        if (this.messageManager)
            this.messageManager.send(new Mdt.WordCategoryInfoRequest());
    }

    public mounted() {
        // @ts-ignore
        this.$refs.computeButton.registerGlobalEnterKey();
        const ip = "http://" + window.location.hostname + ":5001/similarity_ranker";
        this.messageManager = new MessageManager(this.updateOnMessage, ip);


        this.sendInfoRequest();
        // retry connection to retrieve info every 10 seconds
        const intervalId = setInterval(() => {
            console.log('sending info request');
            if (this.infoReceived) {
                clearInterval(intervalId);
                return;
            }
            this.sendInfoRequest();
        }, 10000);

        // @ts-ignore
        this.$refs.computeButton.onCompute = () => {
            let reqData = this.collectRequestData();
            console.log(reqData);
            if (reqData !== null) {
                // @ts-ignore
                this.$refs.simRankGraph.chart.chart.showLoading();
                this.messageManager!.send(reqData);
            }
            else
                // @ts-ignore
                this.$refs.computeButton.reset();
        };
    }

}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

body {
  padding: 30px;
  background-color: rgba(41,52,65,1);
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-box-pack: start;
  -ms-flex-pack: start;
  justify-content: flex-start;
  font-weight: 600;
  letter-spacing: 2px;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 5ch;
  width: 1000px;
}

h1 {
  margin-left: auto;
  margin-right: auto;
  font-size: 2.5rem;
  max-width: 500px;
  letter-spacing: 3px;
  text-align: center;
  line-height: 1.5;
  font-weight: 800;
  color: navajowhite;
}

h1 span {
  color: #FF908B;
}

div.input-div {
  text-align: center;
  margin-top: 1ch;
  position: relative;
}

.word-di {
  top: 5%;
  left: 1%;
  width: 15rem;
  margin-top: 8vh;
  position: absolute;
  z-index: 1000;
}
.category-di {
  top: 5%;
  left: 32%;
  width: 15rem;
  margin-top: 8vh;
  position: absolute;
  z-index: 1000;
}

.count-ib {
  top: 5%;
  left: 58%;
  width: 15rem;
  margin-top: 8vh;
  position: absolute;
}

.compute-button {
  left: 85%;
  width: 10rem;
  height: inherit;
  margin-top: 10vh;
  position: absolute;
  border:0;
  padding:0;
  cursor:pointer;
  font-size: 1rem;
  font-weight:bold;
  color:rgba(0,0,0,0);
  background:transparent;
  border-radius:.25rem;
  -webkit-tap-highlight-color: rgba(0,0,0,0);
  -webkit-touch-callout: none;
}

</style>
