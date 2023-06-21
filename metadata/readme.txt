This program allows you to update spelling and trait names for off chain data for solana nfts. 

to start, use cryptostraps tools to pull your metadata file for your collection, and replace metadata.json

in metadata.py notice the replace dictionary, this is where you put your old names and replacements, spelling and capitalization must be exact. ""Old Name":"New Name"" this is currently set to replace both trait types and trait names, so if you have any trait names that match the trait names you will want to modify this code to make sure you dont change the wrong thing. 

once you have written your replace dict run "python3 metadata.py" (from terminal, in this directory) this will take a little bit of time, as it goes make sure to spot check to make sure there was no mistakes. 

after this is complete your updated_metadata will have all of your fixed data. 

make sure you have metaboss, and the solana cli installed and set your solana cli config to the update authority of the collection, and set a custom rpc endpoint as the mainnet one will not work. 

replace the arweave keypair file with your own arweave keypair loaded with enough AR to complete the job. 

run "python3 updatemetadata.py", let the program run, this will take some time. 

you are complete.
