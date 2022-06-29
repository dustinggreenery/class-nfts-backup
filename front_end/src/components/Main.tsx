import { useEthers } from '@usedapp/core'
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants } from 'ethers'
import brownieConfig from "../brownie-config.json"

export const Main = () => {
    const { chainId, error } = useEthers()
    const networkName = chainId ? helperConfig[chainId] : "dev"

    const classNFTAddress = chainId ? networkMapping[String(chainId)]["ClassNFT"][0] : constants.AddressZero
    const vrfCoordinatorAddress = chainId ? brownieConfig["networks"][networkName]["vrf_coordinator"] : constants.AddressZero
    const linkTokenAddress = chainId ? brownieConfig["networks"][networkName]["link_token"] : constants.AddressZero
    const keyHash = chainId ? brownieConfig["networks"][networkName]["keyhash"] : constants.AddressZero
    const fee = chainId ? brownieConfig["networks"][networkName]["fee"] : 100000000000000000

    return (<div>Addresses Saved</div>)
}