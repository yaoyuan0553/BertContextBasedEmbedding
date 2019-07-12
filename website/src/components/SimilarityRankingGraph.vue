<template>
    <div class="sim-result">
        <div ref="graphDiv" id="graph-main"></div>
    </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';
import SimilarityChart from '@/ts-components/SimilarityChart';
import * as echarts from 'echarts';
import { ChalkTheme } from '@/ts-components/EchartThemes';

@Component
export default class SimilarityRankingGraph extends Vue {
    $refs!: {
        graphDiv: HTMLDivElement;
    };

    public chart: SimilarityChart | undefined;

    public created()
    {
        echarts.registerTheme('chalk', ChalkTheme);
    }

    public mounted()
    {
        this.chart = new SimilarityChart(this.$refs.graphDiv, 'chalk');
    }
}

</script>

<style scoped>

.sim-result {
    padding-top: 20ch;
    margin-left: auto;
    margin-right: auto;
}

#graph-main {
    width: 1000px;
    height: 400px;
    margin-top: 10ch;
}

</style>