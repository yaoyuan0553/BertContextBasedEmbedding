<template>
  <div id="app">
    <h1>副词语义相似度计算器</h1>
    <div class="inputDiv">
      <DropdownInput ref="wordDi" class="word-di" title="词汇" placeholder="选择词汇"/>
      <DropdownInput ref="categoryDi" class="category-di" title="类别" placeholder="选择类别"/>
      <ComputeButton ref="computeButton"/>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ComputeButton from './components/ComputeButton.vue';
import DropdownInput from './components/DropdownInput.vue';
import MessageManager from './MessageManager';

const messageManager = new MessageManager((xhr: XMLHttpRequest, ev?: Event) => {
});

@Component({
  components: {
    ComputeButton,
    DropdownInput,
  },
})
export default class App extends Vue {
  public $refs!: {
    computeButton: ComputeButton,
    wordDi: DropdownInput,
    categoryDi: DropdownInput,
  };

  public $mount(elementOrSelector?: Element | string, hydrating?: boolean): this
  {
    let tmp = super.$mount(elementOrSelector, hydrating);
    this.$refs.computeButton.registerGlobalEnterKey();
    return tmp;
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
  margin-top: 60px;
  width: 75%;
}

h1 {
  margin-top: 10vh;
  font-size: 2.5rem;
  max-width: 500px;
  letter-spacing: 3px;
  text-align: center;
  line-height: 1.5;
  text-transform: capitalize;
  font-weight: 800;
  color: floralwhite;
}
h1 span {
  color: #FF908B;
}

.word-di {
  float: left;
  top: 5%;
  left: 2%;
  width: 15rem;
  margin-top: 8vh;
  position: relative;
  z-index: 1000;
}
.category-di {
  float: left;
  top: 5%;
  left: 7%;
  width: 15rem;
  margin-top: 8vh;
  position: relative;
  z-index: 1000;
}

div.inputDiv {
  text-align: center;
  margin-top: 10ch;
  position: relative;
}

</style>
