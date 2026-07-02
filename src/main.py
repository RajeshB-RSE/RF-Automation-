from .instrument import InstrumentController, example_workflow


def main():
    print("Starting RF Automation example workflow")
    result = example_workflow()
    print("Done. Screenshot:", result['screenshot'])
    print("Measurements:")
    for k, v in result['measurements'].items():
        print(f"  {k}: {v}")


if __name__ == '__main__':
    main()
