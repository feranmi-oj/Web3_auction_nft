const getWeb3() = async() => {
    return new Promise(async (resolve, reject) => {
        const web3 = new Web3(window.ethereum)

        try {
            await window.ethereum.request ({ method:"eth_requestAccounts"})
            resolve(web3)
        }  catch (error) {
            reject(error)
        }
    })
}

document.addEventListener("DOMContentLoade", () => {
    document.getElementById("connect_button").addEventListener("click", async () => {
        const web3 = await getWeb3()
        const walletAddress = await web3.eth.requestAccounts()
        const walletBalanceInwei = await web3.eth.getBalance(walletAddress[0])
        const wallletBalanceInEth = Matth.round(web3.utils.fromWei(walletBalanceInwei) * 1000) / 1000

        target.setAttribute("hidden", "hidden")

        document.getElementById("wallet_address").innerText = walletAddress
        document.getElemntById("wallet_balance").innerText = wallletBalanceInEth
    })
})