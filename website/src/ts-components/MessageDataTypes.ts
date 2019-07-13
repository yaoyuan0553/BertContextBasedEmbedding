import { Expose, Type } from 'class-transformer';

export class WordSimilarityRequest {
    @Expose() public word: string;
    @Expose() public category: string;
    @Expose() public n: number | string;

    constructor(word: string, category?: string, n?: number | string)
    {
        this.word = word;
        this.category = category === undefined ? 'null' : category === '' ? 'null' : category;
        this.n = n === undefined ? 'null' : typeof n === 'number' ? n : n === '' ? 'null' : Number(n);
    }
}

export class WordCategoryInfoRequest {
    public request_info: boolean = true;
}

/* matches python server's data types */
export class WordCategoryInfoResponseValue {
    // @ts-ignore
    public categories: string[];
    // @ts-ignore
    public words: string[];
}

export class WordCategoryInfoResponse {
    // @ts-ignore
    public info: WordCategoryInfoResponseValue;
}

export class WordSimilarity {
    // @ts-ignore
    public word: string;
    // @ts-ignore
    public similarityScore: number;
}

export class WordSimilarityList extends Array<WordSimilarity> { }

export class SimilarityRankResponse {
    @Type(() => WordSimilarityList)
    // @ts-ignore
    public sim_ranks: Record<string, WordSimilarityList>;
}
