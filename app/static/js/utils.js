export const quaggaConfig = {
    inputStream : {
        name : "Live",
        type : "LiveStream",
        constraints: {
            width: 800,
            height: 450
        },
    },
    decoder : {
        readers : ["code_128_reader"]
    }
}