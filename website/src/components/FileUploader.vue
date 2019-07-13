<template>
<!--    <div class="file-uploader">-->
<!--      <div class="table">-->
<!--          <div class="table-cell">-->
<!--              <button class="close-button" @click="toggleMenu">&times;</button>-->
<!--              <div class="modal">-->
<!--                  <div id="profile" @dragover="onDragOver" @dragleave="onDragLeave" @drop="onDrop" @click="onClick">-->
<!--                      <div class="dashes"></div>-->
<!--                      <label>Click to browse or drag an image here</label></div>-->
<!--                  <div class="editable"><i class="fa fa-pencil"></i></div>-->
<!--                  <button class="submit-button">Done Editing</button>-->
<!--              </div>-->
<!--          </div>-->
<!--      </div>-->
<!--      <input ref="mediaFile" @change="onMediaFileChange" type="file" id="mediaFile" />-->
        <input id="input-id" type="file" class="file">
<!--    </div>-->
</template>

<script lang='ts'>

import {Component, Vue} from 'vue-property-decorator';

@Component
export default class FileUploader extends Vue {

    $refs!: {
        mediaFile: HTMLInputElement;
    };

    public toggleMenu()
    {
        $('.file-uploader').toggleClass('show-menu');
    }

    onDragOver()
    {
        $('#profile').addClass('dragging');
    }
    onDragLeave()
    {
        $('#profile').removeClass('dragging');
    }

    onDrop(e?: DragEvent)
    {
        $('#profile').removeClass('dragging hasFile');

        if (e)
        {
            const file = e.dataTransfer!.files[0];
            console.log(file);

            let reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e: Event) => {
                $('#profile').css('background-image', 'url(' + reader.result + ')').addClass('hasFile');
            };
        }
    }

    onClick()
    {
        console.log('clicked');
        $('#mediaFile').click();
    }

    onMediaFileChange()
    {
        if (this.$refs.mediaFile.files && this.$refs.mediaFile.files[0]) {
            const reader = new FileReader();
            reader.readAsDataURL(this.$refs.mediaFile.files[0]);
            reader.onload = (e: Event) => {
                $('#profile').css('background-image', 'url(' + reader.result + ')').addClass('hasFile');
            }
        }
    }

    created()
    {
    }

    mounted()
    {
        console.log('file uploader', this);
/*
        $('#profile').addClass('dragging').removeClass('dragging');

        window.addEventListener('dragover', (e?: Event) => {
            if (e) {
                e.preventDefault();
            }
        }, false);

        window.addEventListener('drop', (e?: Event) => {
            if (e) {
                e.preventDefault();
            }
        }, false);*/

        $('#input-id').fileinput({
            allowedFileExtensions: ["jpg", "gif", "png", "txt"],
            theme: 'fas'
        });
    }
}

</script>

<style lang="scss" scoped>
// ----- Personal preference -----
*, *:before, *:after {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}

.file-uploader {
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    position: fixed;
    z-index: 1100;
    background-color: rgba(0, 0, 0, 0.5);
    opacity: 0;
    visibility: hidden;
    transform: scale(1.1);
    transition: visibility 0s linear 0.25s, opacity 0.25s 0s, transform 0.25s;
}

// ----- Variable Declarations -----
@keyframes spin {
    from {transform:rotate(0deg);}
    to {transform:rotate(360deg);}
}

.table {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: table;
    width: 300px;
    height: 300px;
    position: absolute;
}
.table-cell {
    display: table-cell;
    vertical-align: middle;
}
.modal {
    width: 300px;
    height: 300px;
    margin: 0 auto;
    background: #fff;
    box-shadow: 0 40px 50px rgba(black, 0.35);
    padding: 40px;
    -webkit-border-radius: 0.5rem;
    -moz-border-radius: 0.5rem;
    border-radius: 0.5rem;
}
#mediaFile {
    position: absolute;
    top: -1000px;
    visibility: hidden;
    opacity: 0;
}
#profile {
    border-radius: 100%;
    width: 200px;
    height: 200px;
    margin: 0 auto;
    position: relative;
    top: -80px;
    margin-bottom: -80px;
    cursor: pointer;
    background: #f4f4f4;
    display: table;
    background-size: cover;
    background-position: center center;
    box-shadow: 0 5px 8px rgba(black, 0.35);
    .dashes {
        position: absolute;
        top: 0;
        left: 0;
        border-radius: 100%;
        width: 100%;
        height: 100%;
        border: 4px dashed #ddd;
        opacity: 1;
    }
    label {
        display: table-cell;
        vertical-align: middle;
        text-align: center;
        padding: 0 30px;
        color: grey;
        opacity: 1;
    }
    &.dragging {
        background-image: none!important;
        .dashes {
            animation-duration: 10s;
            animation-name: spin;
            animation-iteration-count:infinite;
            animation-timing-function: linear;
            opacity: 1!important;
        }
        label {
            opacity: 0.5!important;
        }
    }
    &.hasFile {
        .dashes, label {
            opacity: 0;
            pointer-events: none;
            user-select: none;
        }
    }
}
h1 {
    text-align: center;
    font-size: 28px;
    font-weight: normal;
    letter-spacing: 1px;
}
.stat {
    width: 50%;
    text-align: center;
    float: left;
    padding-top: 20px;
    border-top: 1px solid #ddd;
    .label {
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase
    }
    .num {
        font-size: 21px;
        padding: 3px 0;
    }
}
.editable {
    position: relative;
    i {
        position: absolute;
        top: 10px;
        right: -20px;
        opacity: 0.3
    }
}
button.submit-button {
    width: 100%;
    -webkit-appearance: none;
    line-height: 40px;
    color: #fff;
    border: none;
    -webkit-border-radius: 0.5rem;
    -moz-border-radius: 0.5rem;
    border-radius: 0.5rem;
    background-color: #ea4c89;
    margin-top: 50px;
    font-size: 13px;
    -webkit-font-smoothing: antialiased;
    font-weight: bold;
    letter-spacing: 1px;
    text-transform: uppercase
}

button.close-button {
    float: right;
    width: 1.5rem;
    line-height: 1.5rem;
    text-align: center;
    cursor: pointer;
    border-radius: 0.3rem;
    border-color: transparent;
    background-color: lightgray;
}

button.close-button:hover {
    background-color: darkgray;
}

.show-menu {
    opacity: 1;
    visibility: visible;
    transform: scale(1.0);
    transition: visibility 0s linear 0s, opacity 0.25s 0s, transform 0.25s;
}

// ----- Mobile styles -----
@media only screen
and (max-device-width: 736px) {
}

</style>