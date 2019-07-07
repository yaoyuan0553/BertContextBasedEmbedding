import { plainToClass } from "class-transformer"
import { MessageManager } from "./MessageManager";
import { WordCategoryInfoResponseValue, WordCategoryInfoResponse } from "./MessageDataType"


function handleInfoResponse(xhr: XMLHttpRequest)
{
    if (xhr.readyState === 4 && xhr.status === 200) {

    }
}

const jsonInfo = {
    "info": {
        "categories": ["blah", "blah", "okay", "not"],
        "words": ["word1", "word2"]
    }
}

let infoVal = plainToClass(WordCategoryInfoResponse, jsonInfo);

console.log(infoVal);
