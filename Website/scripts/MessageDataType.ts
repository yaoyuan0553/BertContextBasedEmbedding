import {Expose, Type} from "class-transformer";

export class WordSimilarityRequest {
    @Expose() word: string;
    @Expose() category: string;
    @Expose() n: number;

    constructor(word: string, category?: string, n?: number)
    {
        this.word = word;
        this.category = category === undefined ? null : category;
        this.n = n === undefined ? null : n;
    }
}

export class WordCategoryInfoRequest {
    request_info: boolean = true;
}

/* matches python server's data types */
export class WordCategoryInfoResponseValue {
    categories: string[];
    words: string[];
}

export class WordCategoryInfoResponse {
    info: WordCategoryInfoResponseValue;
}

export class WordSimilarity {
    word: string;
    similarityScore: number;
}

export class WordSimilarityList extends Array<WordSimilarity> { }

export class SimilarityRankResponse {
    @Type(() => WordSimilarity)
    sim_ranks: Map<string, WordSimilarityList>;
}

