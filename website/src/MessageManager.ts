import {classToPlain, plainToClass} from 'class-transformer';
import * as Mdt from '@/components/MessageDataTypes';

export default class MessageManager {

    public url: string;

    private readonly xhr: XMLHttpRequest;

    constructor(receiveCallback: (xhr: XMLHttpRequest, ev?: Event) => void,
                url = 'http://0.0.0.0:5001/similarity_ranker')
    {
        this.url = url;
        this.xhr = new XMLHttpRequest();
        this.xhr.onreadystatechange = (ev?: Event) => { receiveCallback(this.xhr, ev); };
    }

    public send(data: Mdt.WordSimilarityRequest | Mdt.WordCategoryInfoRequest)
    {
        const test = classToPlain(data);
        console.log('converted:', test);
        const msg: string = JSON.stringify(classToPlain(data));
        console.log(msg);
        this.xhr.open('POST', this.url, true);
        this.xhr.setRequestHeader('Content-Type', 'application/json');
        this.xhr.send(msg);
    }

    public test()
    {
        const wsr = {
            word: 'okay',
            category: 'xx',
            n: 3,
        };
        const wsrObject = plainToClass(Mdt.WordSimilarityRequest, wsr);

        const wsl = [{word: 'okay', similarityScore: 12}, {word: 'blah', similarityScore: 33}];
        const wslObject = plainToClass(Mdt.WordSimilarityList, wsl);

        // console.log(wsl);
        // console.log(wslObject);

        const srr = { sim_ranks: {'#12成都': wsl}};
        const srrObject = plainToClass(Mdt.SimilarityRankResponse, srr);

        console.log(srr);
        console.log(srrObject);
        for (let cat in srrObject.sim_ranks) {
            console.log(cat);
            let catSimRanks = srrObject.sim_ranks[cat];
            for (let i = 0; i < catSimRanks.length; i++) {
                console.log(catSimRanks[i]);
            }
        }
    }
}
