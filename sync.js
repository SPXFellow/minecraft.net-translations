const https = require('https')
const { promises: fs } = require('fs')
const path = require('path')

const UsernamePath = path.join(__dirname, 'username.json')
const RawTablePath = path.join(__dirname, 'rawtable.csv')
const McbbsIndexUri = 'https://www.mcbbs.net/thread-823054-1-1.html'

let count = 0

/**
 * @type {{[username: string]: string}}
 */
let username = {}
/**
 * @type {string[][]}
 */
const rawTable = []

/**
 * @param {string} uri
 * @returns {Promise<string>}
 */
async function get(uri) {
    return new Promise((resolve, reject) => {
        https.get(uri, res => {
            let data = ''
            res
                .on('data', chunk => data += chunk)
                .on('end', () => resolve(data))
                .on('error', err => reject(err))
        })
    })
}

async function loadUsername() {
    const content = await fs.readFile(UsernamePath, { encoding: 'utf8' })
    username = JSON.parse(content)
}

async function saveUsername() {
    const content = JSON.stringify(username, Object.keys(username).sort(), 4)
    await fs.writeFile(UsernamePath, content, { encoding: 'utf8' })
}

async function loadRawTable() {
    const content = await fs.readFile(RawTablePath, { encoding: 'utf8' })
    const rows = content.split(/\r?\n/)
    for (const row of rows) {
        // https://stackoverflow.com/questions/21105360/regex-find-comma-not-inside-quotes/21106122
        rawTable.push(row.split(/(?!\B"[^"]*),(?![^"]*"\B)/))
    }
}

async function saveRawTable() {
    const content = rawTable.map(c => c.join(',')).join('\n')
    await fs.writeFile(RawTablePath, content, { encoding: 'utf8' })
}

/**
 * @param {string} un
 * @param {string} link
 */
async function getAuthorUid(un, link) {
    try {
        if (username[un]) {
            return username[un]
        }
        const regex = /<div class="authi"><a href="home\.php\?mod=space&amp;uid=(\d+?)"/
        const html = await get(link)
        const [, uid] = regex.exec(html)
        username[un] = uid
        return uid
    }
    catch (e) {
        console.error(e)
        return ''
    }
}

async function merge() {
    try {
        const regex = /<a href="https?:\/\/(?:www\.)?minecraft\.net\/.+?\/article\/(.+?)" target="_blank">.+?<\/a><\/td><td width="30%"><a href="(.+?)" target="_blank">(.+?)<\/a><\/td><td width="25%">(.+?)<\/td><\/tr>/g

        const html = await get(McbbsIndexUri)
        let match = regex.exec(html)
        while (match) {
            const [, link, trLink, trTitle, trUsername] = match
            if (/^https?:\/\/(?:www\.)?mcbbs\.net\/thread\-\d+\-\d+\-\d+\.html?$/.test(trLink) && trUsername !== '-') {
                const row = rawTable.find(r => r[2] && r[2].endsWith(link))
                if (row) {
                    if (row[4] !== trLink) {
                        console.log(`${link}: ${row[4]} -> ${trLink} (${trUsername})`)
                        try {
                            row[5] = await getAuthorUid(trUsername, trLink)
                            row[3] = trTitle
                            row[4] = trLink
                            row[6] = '1'
                            count++
                        } catch (e) {
                            console.error(e)
                        }
                    }
                } else {
                    console.warn(`Faild to find article ‘${link}’ in the raw table.`)
                }
            }
            match = regex.exec(html)
        }
    } catch (e) {
        console.error(e)
    }
}

async function sync() {
    try {
        const start = new Date().getTime()
        await loadRawTable()
        // await loadUsername()
        await merge()
        // await saveUsername()
        await saveRawTable()
        console.log(`Successfully synchronised ${count} article(s) in ${new Date().getTime() - start}ms!`)
    } catch (e) {
        console.error(e)
    }
}

Promise
    .race(sync(), new Promise(resolve => setTimeout(resolve, 60_000)))
    .then(() => {
        console.log("Process exit.")
        process.exit()
    })
