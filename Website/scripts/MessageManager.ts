import {classToPlain} from "class-transformer";
import {WordSimilarityRequest, WordCategoryInfoRequest} from "./MessageDataType";

class MessageManager {
    xhr: XMLHttpRequest;
    url: string;

    constructor(url = "http://0.0.0.0:5001/similarity_ranker",
                receiveCallback: (xhr: XMLHttpRequest, ev?: Event) => void)
    {
        this.url = url;
        this.xhr = new XMLHttpRequest();
        this.xhr.onreadystatechange = (ev?: Event) => { receiveCallback(this.xhr, ev); };
    }

    send(data: WordSimilarityRequest | WordCategoryInfoRequest)
    {
        let msg = JSON.stringify(classToPlain(data));
        this.xhr.open("POST", this.url, true);
        this.xhr.setRequestHeader("Content-Type", "application/json");
        this.xhr.send(msg);
    }

}