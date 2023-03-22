const {  
  loadFixture,
} = require("@nomicfoundation/hardhat-network-helpers");

const { expect, assert } = require("chai");

describe("Institution", function () {
  // We define a fixture to reuse the same setup in every test.
  // We use loadFixture to run this setup once, snapshot that state,
  // and reset Hardhat Network to that snapshot in every test.
  async function deployInstitutionFixture() {
    [owner, student1, student2] = await ethers.getSigners();

    const Institution = await ethers.getContractFactory("Institution");
    let institution = await Institution.deploy(true);
    await institution.deployed();

    const StorageAwards = await ethers.getContractFactory("StorageAwards");
    const addressStorageAwards = await institution.getStorageAwards();
    let storageAwards = await StorageAwards.attach(addressStorageAwards);

    return { owner, student1, student2, institution, storageAwards };
  }

  async function addAward(
    student,
    institution,
    awardTitle,
    awardDate,
    nonceAwardSign,
    chainid
  ) {
    const messageHash = ethers.utils.solidityKeccak256(
      ["string", "uint", "uint", "uint", "address"],
      [awardTitle, awardDate, nonceAwardSign, chainid, institution.address]
    );
    const messageHashBinary = ethers.utils.arrayify(messageHash);
    const signature = await student.signMessage(messageHashBinary);

    //console.log("student address:",student.address);
    await institution.addAwardSignedByStudent(
      signature,
      student.address,
      awardTitle,
      awardDate
    );
  }

  it("Not Contains Student", async function () {
    const { student1, storageAwards } = await loadFixture(
      deployInstitutionFixture
    );
    const containsStudent = await storageAwards.containsStudent(
      student1.address
    );
    expect(containsStudent).to.equal(false);
  });

  it("Add Awards", async function () {
    const { institution, storageAwards, student1, student2 } =
      await loadFixture(deployInstitutionFixture);
    const chainid = await student1.getChainId();

    //add awards for student 1
    await addAward(
      student1,
      institution,
      "Student 1 is first in class",
      1666936687,
      0,
      chainid
    );
    await addAward(
      student1,
      institution,
      "Student 1 - award for participation",
      1666936688,
      1,
      chainid
    );

    //check for student 1
    const containsStudent = await storageAwards.containsStudent(
      student1.address
    );
    expect(containsStudent).to.equal(true);

    let numberOfStudents = await storageAwards.numberOfStudents();
    expect(numberOfStudents).to.equal(1);

    let numberOfAwards = await storageAwards.getStudentAwardsCount(
      student1.address
    );
    expect(numberOfAwards).to.equal(2);

    let award = await storageAwards.getStudentAward(student1.address, 1);
    assert(award != null);
    expect(award.title).to.equal("Student 1 - award for participation");
    expect(award.date).to.equal(1666936688);

    //add award for student2
    await addAward(
      student2,
      institution,
      "Student 2 - award",
      1666936688,
      0,
      chainid
    );

    //check for student 2
    numberOfStudents = await storageAwards.numberOfStudents();
    expect(numberOfStudents).to.equal(2);

    numberOfAwards = await storageAwards.getStudentAwardsCount(
      student2.address
    );
    expect(numberOfAwards).to.equal(1);

    award = await storageAwards.getStudentAward(student2.address, 0);
    assert(award != null);
    expect(award.title).to.equal("Student 2 - award");
    expect(award.date).to.equal(1666936688);
  });

  it("Remove Award", async function () {
    const { institution, storageAwards, student1, student2 } =
      await loadFixture(deployInstitutionFixture);
    const chainid = await student1.getChainId();

    //add awards for student 1
    await addAward(student1, institution, "Award_Test", 1666936687, 0, chainid);

    //check that award was added correctly
    let award = await storageAwards.getStudentAward(student1.address, 0);
    assert(award != null);
    expect(award.title).to.equal("Award_Test");

    let awards_count = await storageAwards.getStudentAwardsCount(
      student1.address
    );
    expect(awards_count).to.equal(1);

    //remove award
    institution.removeAward(student1.address, 0);

    //check that award no longer exists
    awards_count = await storageAwards.getStudentAwardsCount(student1.address);
    expect(awards_count).to.equal(0);

    await expect(storageAwards.getStudentAward(student1.address, 0)).to.be
      .reverted;
  });

  it("Remove Student Data", async function () {
    const { institution, storageAwards, student1, student2 } =
      await loadFixture(deployInstitutionFixture);
    const chainid = await student1.getChainId();

    //add awards for student 1
    await addAward(student1, institution, "Award_Test", 1666936687, 0, chainid);

    //check that award was added correctly
    let award = await storageAwards.getStudentAward(student1.address, 0);
    assert(award != null);
    expect(award.title).to.equal("Award_Test");

    //check that student was added
    let numbOfStudents = await storageAwards.numberOfStudents();
    expect(numbOfStudents).to.equal(1);

    let awards_count = await storageAwards.getStudentAwardsCount(
      student1.address
    );
    expect(awards_count).to.equal(1);

    //remove data
    institution.removeStudentData(student1.address);

    //check that award no longer exists
    awards_count = await storageAwards.getStudentAwardsCount(student1.address);
    expect(awards_count).to.equal(0);
    await expect(storageAwards.getStudentAward(student1.address, 0)).to.be
      .reverted;

    //check that student no longer exists
    numbOfStudents = await storageAwards.numberOfStudents();
    expect(numbOfStudents).to.equal(0);
    await expect(storageAwards.getStudentAt(0)).to.be.reverted;
  });

  //-----------Test for permissons---------

  it("Access Directly StorageAwards", async function () {
    const { storageAwards, student1, institution } = await loadFixture(
      deployInstitutionFixture
    );

    await expect(
      storageAwards.addStudentAward(student1.address, "title", 000)
    ).to.be.revertedWith("call not made by latest address version");
    await expect(
      storageAwards.removeStudentAward(student1.address, 0)
    ).to.be.revertedWith("call not made by latest address version");
    await expect(
      storageAwards.removeStudentData(student1.address)
    ).to.be.revertedWith("call not made by latest address version");
   

  });

 

  it("Permissions Institution", async function () {
    const { institution, student1 } = await loadFixture(
      deployInstitutionFixture
    );

    //a non-owner tries to add an award
    const chainid = await student1.getChainId();
    const awardTitle = "Student 1 is first in class";
    const awardDate = 1666936687;
    const nonceAwardSign = 0;

    const messageHash = ethers.utils.solidityKeccak256(
      ["string", "uint", "uint", "uint", "address"],
      [awardTitle, awardDate, nonceAwardSign, chainid, institution.address]
    );
    const messageHashBinary = ethers.utils.arrayify(messageHash);
    const signature = await student1.signMessage(messageHashBinary);

    await expect(
      institution
        .connect(student1)
        .addAwardSignedByStudent(
          signature,
          student1.address,
          awardTitle,
          awardDate
        )
    ).to.be.revertedWith("Ownable: caller is not the owner");

    //a non-owner tries to remove award
    await expect(
      institution.connect(student1).removeAward(student1.address, 0)
    ).to.be.revertedWith("Ownable: caller is not the owner");

    //a non-owner tries to remove student data
    await expect(
      institution.connect(student1).removeStudentData(student1.address)
    ).to.be.revertedWith("Ownable: caller is not the owner");

    //a non-owner tries to change storage address
    await expect(
      institution.connect(student1).setStorageAwards(student1.address)
    ).to.be.revertedWith("Ownable: caller is not the owner");
  });


  it("Changing owner StorageAwards", async function () {
    const { storageAwards, student1, institution } = await loadFixture(
      deployInstitutionFixture
    );

    //deploy new institution contract & change latest version in storageAwards
    const InstitutionUpdated = await ethers.getContractFactory("Institution");
    let institutionUpdated = await InstitutionUpdated.deploy(false);
    await institutionUpdated.deployed();

    await institutionUpdated.setStorageAwards(storageAwards.address);
    await institution.upgradeStorageAwardsOwner(institutionUpdated.address);

    //try to add award
    const chainid = await student1.getChainId();
    const awardTitle = "Student 1 is first in class";
    const awardDate = 1666936687;
    const nonceAwardSign = 0;

    let messageHash = ethers.utils.solidityKeccak256(
      ["string", "uint", "uint", "uint", "address"],
      [awardTitle, awardDate, nonceAwardSign, chainid, institution.address]
    );
    let messageHashBinary = ethers.utils.arrayify(messageHash);
    let signature = await student1.signMessage(messageHashBinary);

    //an old institute contract tries to add award
    await expect(
      institution        
        .addAwardSignedByStudent(
          signature,
          student1.address,
          awardTitle,
          awardDate
        )
    ).to.be.revertedWith("call not made by latest address version");

    //latest institute contract tries to add award

    messageHash = ethers.utils.solidityKeccak256(
      ["string", "uint", "uint", "uint", "address"],
      [awardTitle, awardDate, nonceAwardSign, chainid, institutionUpdated.address]
    );
    messageHashBinary = ethers.utils.arrayify(messageHash);
    signature = await student1.signMessage(messageHashBinary);

    await institutionUpdated        
    .addAwardSignedByStudent(
      signature,
      student1.address,
      awardTitle,
      awardDate
    )
  
    let numberOfAwards = await storageAwards.getStudentAwardsCount(
      student1.address
    );
    expect(numberOfAwards).to.equal(1);

    //an old institute contract tries to remove award
    await expect(
      institution.removeAward(student1.address, 0)
    ).to.be.revertedWith("call not made by latest address version");

    //an old institute contract tries to remove student data
    await expect(
      institution.removeStudentData(student1.address)
    ).to.be.revertedWith("call not made by latest address version");

  });

});
