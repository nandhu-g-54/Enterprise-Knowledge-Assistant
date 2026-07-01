from answer import ask

while True:

    question = input("\nAsk : ")

    if question.lower() == "exit":
        break

    result = ask(question)

    print("\n")

    print("=" * 70)

    print(result["answer"])

    print()

    print("Confidence :")

    print(result["confidence"])

    print()

    print("Sources :")

    for s in result["sources"]:

        print(s)

    print("=" * 70)