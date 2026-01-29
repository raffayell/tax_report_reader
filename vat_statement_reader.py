import camelot
import pandas as pd


def get_vat_tables(path: str) -> camelot.core.TableList:
    tables = camelot.read_pdf(path, suppress_stdout=True,
                              pages="all")
    stmnt_name = tables[0].df[0][0].replace('\n', "")
    if "ՄԻԱՍՆԱԿԱՆ ՀԱՇՎԱՐԿԱՎԵԼԱՑՎԱԾ ԱՐԺԵՔԻ ՀԱՐԿԻ ԵՎԱԿՑԻԶԱՅԻՆ ՀԱՐԿԻ" not in stmnt_name:
        raise ValueError("Incorrect statement")
    return tables

def get_company(tables: camelot.core.TableList) -> dict:
    df: pd.DataFrame = tables[0].df
    company: str = df[1][3]
    tin: str = df[0][2].replace('\n', "")
    res: dict = {"Company": company, "TIN": tin}
    return res

def get_period(tables: camelot.core.TableList) -> dict:
    df: pd.DataFrame = tables[0].df
    period: str = df[1][5].replace('\n', "")
    year: int = int(period[4:8])
    month: int = int(period[12:])
    res: dict = {"Year": year, "Month": month}
    return res

def get_credit_data(tables: camelot.core.TableList) -> dict:
    df: pd.DataFrame = tables[1].df
    revenue = df[1][21].replace(",", "")
    if not revenue:
        revenue = 0
    revenue = int(revenue)

    vat_credit = df[2][21].replace(",", "")
    if not vat_credit:
        vat_credit = 0
    vat_credit = int(vat_credit)

    return {"Revenue": revenue, "VAT_credit": vat_credit}

def get_debit_data(tables: camelot.core.TableList) -> dict:
    df: pd.DataFrame = tables[1].df
    import_amount = df[1][23].replace(",", "")
    import_vat = df[2][23].replace(",", "")
    inner_purchase_amount = df[1][24].replace(",", "")
    inner_purchase_vat = df[2][24].replace(",", "")
    if not import_amount:
        import_amount = 0
    if not import_vat:
        import_vat = 0
    if not inner_purchase_amount:
        inner_purchase_amount = 0
    if not inner_purchase_vat:
        inner_purchase_vat = 0
    import_amount = int(import_amount)
    import_vat = int(import_vat)
    inner_purchase_amount = int(inner_purchase_amount)
    inner_purchase_vat = int(inner_purchase_vat)
    
    return {
        "Import amount": import_amount, "Import VAT": import_vat,
        "Inner purchase amount": inner_purchase_amount,
        "Inner purchase VAT": inner_purchase_vat
        }


def get_vat_total(tables: camelot.core.TableList) -> dict:
    df: pd.DataFrame = tables[2].df
    vat_total_credit = df[1][5].replace(",", "")
    vat_total_debit = df[2][5].replace(",", "")
    if not vat_total_credit:
        vat_total_credit = 0
    if not vat_total_debit:
        vat_total_debit = 0
    vat_total_credit = int(vat_total_credit)
    vat_total_debit = int(vat_total_debit)
    if vat_total_credit == 0 and vat_total_debit == 0:
        return {"VAT total": 0}
    if vat_total_credit > 0:
        return {"VAT total": vat_total_credit}
    if vat_total_debit > 0:
        return {"VAT total": vat_total_debit * -1}