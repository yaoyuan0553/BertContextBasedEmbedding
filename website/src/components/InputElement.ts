import Vue from 'vue';

export default class InputElement extends Vue {
    $refs!: {
        inputBox: HTMLInputElement;
    };

    value() {
        return this.$refs.inputBox.value;
    }
}
