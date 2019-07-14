<template>
    <!-- Modal -->
    <div class="modal fade" id="fileUploadModal" tabindex="-1" role="dialog" aria-labelledby="fileUploadModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="fileUploadModalLabel">上传字典文件</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="file-loading">
                        <input id="input-b9" name="input-b9[]" type="file" accept=".txt">
                    </div>
                    <div id="kartik-file-errors"></div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">关闭</button>
                    <button type="button" class="btn btn-primary" title="Your custom upload logic">上传</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang='ts'>

import {Component, Vue} from 'vue-property-decorator';

@Component
export default class TxtFileInput extends Vue {
    mounted()
    {
        $('#input-b9').fileinput({
            elErrorContainer: '#kartik-file-errors',
            allowedFileExtensions: ['txt'],
            theme: 'fas',
            language: 'zh',
            previewFileType: 'text',
            maxFileCount: 1,
            dropZoneTitle: '拖拽字典文件到这里...',
        })
    }
}

</script>

<style scoped>

</style>