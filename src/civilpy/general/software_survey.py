"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pandas as pd


main_excel_file = r"C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\res\temp\Software Survey.xlsx"
pd.set_option("display.max_rows", 500)


def get_dataframe_for_user(username="Dane Parks", excel_file=main_excel_file):
    """
    A helper function that takes an Excel file created by users running the command:

    `Get-WmiObject -Class Win32_Product | Out-File C:\Temp\applications.csv; echo "Done"`

    In powershell and copying the output results to a tab within an Excel file.

    Parameters
    ----------
    username : The Username of the person you want to retrieve a dataframe for.
    excel_file : The Path location/raw string location of the Excel file you want to extract the information from

    Returns
    -------
    user_applications : a Pandas dataframe containing the results for the specified user
    """
    xl = pd.ExcelFile(excel_file)

    df = xl.parse(username)
    df = df.iloc[1:]

    # Load Each Field into a dataframe
    ids = df.iloc[::6, :].reset_index().drop(columns="index")
    names = df.iloc[1::6, :].reset_index().drop(columns="index")
    vendors = df.iloc[2::6, :].reset_index().drop(columns="index")
    versions = df.iloc[3::6, :].reset_index().drop(columns="index")
    captions = df.iloc[4::6, :].reset_index().drop(columns="index")

    # Combine the fields and relabel the columns
    cleaned_data = pd.concat(
        [ids, names, vendors, versions, captions], ignore_index=True, axis=1
    )
    cleaned_data.rename(
        columns={0: "ID", 1: "Name", 2: "Vendor", 3: "Version", 4: "Caption"},
        inplace=True,
    )

    # Cleaning up the values (removes the values prior to the ':' symbol)
    cleaned_data["ID"] = cleaned_data["ID"].apply(lambda x: x.split(":")[1])
    cleaned_data["Name"] = cleaned_data["Name"].apply(lambda x: x.split(":")[1])
    cleaned_data["Vendor"] = cleaned_data["Vendor"].apply(lambda x: x.split(":")[1])
    cleaned_data["Version"] = cleaned_data["Version"].apply(lambda x: x.split(":")[1])
    cleaned_data["Caption"] = cleaned_data["Caption"].apply(lambda x: x.split(":")[1])

    # Add a column for the User name for later
    cleaned_data["User"] = username

    # Get the dataframe of systems applications and remove them from each user
    system_applications_xcel = pd.ExcelFile(
        r"C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\res\temp\system_applications.xlsx"
    )
    system_applications = system_applications_xcel.parse("Sheet1")
    user_applications = cleaned_data[~cleaned_data.ID.isin(system_applications.ID)]

    return user_applications


def software_survey(excel_file_location=main_excel_file):
    """
    Utilizes the result of `get_data_frame_for_user` function to compile multiple sheets of an Excel file
    from Windows powershell

    Parameters
    ----------
    excel_file_location : The path / raw string filepath to the location of the Excel file containing all the users
                            software lists sorted into tabs named after the user

    Returns
    -------
    Prints a summary of the results displaying each unique software installed on users computers, as well as the
    versions and who has which version installed.
    """
    full_dataset = pd.DataFrame()
    xl = pd.ExcelFile(excel_file_location)

    # Apply the above function to each user
    for user in xl.sheet_names:
        user_dataframe = get_dataframe_for_user(user, main_excel_file)

        full_dataset = pd.concat(
            [full_dataset, user_dataframe], ignore_index=True, sort=False
        )

    for value in full_dataset["Name"].sort_values().unique():
        x = full_dataset[full_dataset["Name"] == value]["Name"].values[0]
        if x == " ":
            pass
        else:
            print(
                f"{full_dataset[full_dataset['Name'] == value]['Name'].values[0]}:\n\tVersions:{', '.join(str(i) for i in full_dataset[full_dataset['Name'] == value]['Version'].unique())}"
            )

            for version in full_dataset[full_dataset["Name"] == value][
                "Version"
            ].unique():
                print(
                    f"\tVersion: {version} - Users: {', '.join(str(i) for i in full_dataset[full_dataset['Version'] == version]['User'].unique())}"
                )
