# factory-playground

A small target repository for a software factory experiment: GitHub issues labelled `factory` are researched, planned, implemented and turned into pull requests by coding agents, with one human approval in between.

The code is `ledgerlite`, a CSV expense ledger with categories, monthly totals and a command line. It uses the Python standard library only, on purpose: the agents work in a sandbox that cannot install packages.

## Usage

The ledger is a CSV file with the columns `date,amount,category,description`. A negative amount is a refund.

```
python3 -m ledgerlite summary ledger.csv
python3 -m ledgerlite summary ledger.csv --category food
python3 -m ledgerlite categories ledger.csv
python3 -m ledgerlite export ledger.csv sorted.csv
```

`--category` restricts both summary tables to a single category. Matching is
case-insensitive, so `--category Food` and `--category food` are equivalent.

The exported file begins with the same `date,amount,category,description` header, so
it is itself a valid ledger file that can be passed back to any `ledgerlite` command.

## Development

```
make check test
```

`check` compiles every file and runs `tabnanny`; `test` runs the `unittest` suite. CI runs both on every pull request.

## License

Apache-2.0
