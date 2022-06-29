// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract ClassNFT is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Student {
        AAKASH,
        JONPAUL,
        COHEN,
        OAK,
        JOHN,
        EMELIO,
        LUCAS,
        KARYSSA,
        NOAH,
        LARA,
        YAQING,
        BELLE,
        MATTEO,
        JOHAN,
        NATHAN,
        KEVIN,
        RYAN,
        STEPHANIE,
        DALUCHI,
        ADAM,
        AIDEN,
        MATTHIAS,
        MSKEDDY_SPECIAL
    }
    mapping(uint256 => Student) public tokenIdToStudent;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event studentAssigned(uint256 indexed tokenId, Student student);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Student", "ST")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Student student = Student(randomNumber % 23);
        uint256 newTokenId = tokenCounter;
        tokenIdToStudent[newTokenId] = student;
        emit studentAssigned(newTokenId, student);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
