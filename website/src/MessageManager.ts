
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

    public send(data: object)
    {
        const msg = JSON.stringify(data);
        this.xhr.open('POST', this.url, true);
        this.xhr.setRequestHeader('Content-Type', 'application/json');
        this.xhr.send(msg);
    }
}
