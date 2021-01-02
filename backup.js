const axios = require("axios");
const fs = require("fs");
const path = require("path");
require("dotenv").config();

const user = process.env.USER;
const zdURL = process.env.ZENDESK_URL;
const token = process.env.TOKEN;
const locale = "en-US";

function correctdate() {
    const date = new Date(Date.now());
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

const date = correctdate();
const auth = Buffer.from(`${user}:token/${token}`).toString("base64");
const endpoint = `${zdURL}/api/v2/help_center/${locale.toLowerCase()}/articles.json`;
let once = 1;

(async function getDataAndWriteToFile(url, filename) {
    function getCorrectPath(title) {
        const p = path.join(__dirname, filename);
        if (!fs.existsSync(p)) {
            fs.mkdirSync(p)
        }
        return `${p}\\${title}.json`;
    }

    while (url) {
        const response = await (await axios.get(url)).data;
        console.log(response.next_page);

        for (let i = 0; i < response.articles.length; i++) {
            const article = response.articles[i];

            if (!article.body) {
                continue;
            }
            const title = article.title.replace(/[#/?%*{}\\<>\*$!\'":@+`|=]+/g, " ");
            fs.writeFileSync(
                getCorrectPath(title),
                JSON.stringify(article),
                function (err) {
                    console.log(err);
                    if (err) return;
                }
            )
        }
        url = response.next_page;
    }
})(endpoint, date);