# replicate_api_key  = r8_OuBSFNS2cDgmJNOnu1TKBtbzIxasq4j0Cwv0B


import replicate

# input = {
#     "prompt": "Indian Reporter covering tragic incidence at Hotel Taj during terror attack",
#     "temperature": 0.2
# }


# Snowflake model
# for event in replicate.stream(
#     "snowflake/snowflake-arctic-instruct",
#     input=input
# ):
#     print(event, end="")


# output = replicate.run(
#     "meta/codellama-70b-instruct:a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf",
#     input=input
# )
# print("".join(output))


# # image gen
# output = replicate.run(
#     "bytedance/sdxl-lightning-4step:727e49a643e999d602a896c774a0658ffefea21465756a6ce24b7ea4165eba6a",
#     input=input
# )
# print(output)

# upscaling

input = {
    "image": "https://replicate.delivery/pbxt/SHjesIvUJp29EqsAJFCWtewwq10L6UqLH5y7AEG3flrb3UdlA/out-0.png",
    # "prompt": "UHD 4k vogue, a woman resting in a magic pool, face above the surface of the water, red freckles"
}

output = replicate.run(
    "batouresearch/magic-image-refiner:507ddf6f977a7e30e46c0daefd30de7d563c72322f9e4cf7cbac52ef0f667b13",
    input=input
)
print(output)


