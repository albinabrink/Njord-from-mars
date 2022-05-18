import os
import tempfile

from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https//becquerelswedenab.sharepoint.com").with_credentials("Njord@becquerelsweden.se", "Tull854140")# test_client_credentials)
# file_url = '/sites/team/Shared Documents/big_buck_bunny.mp4'
file_url = "/sites/team/Shared Documents/market_size_factors.xlsx"
download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_url))
with open(download_path, "wb") as local_file:
    file = ctx.web.get_file_by_server_relative_path(file_url).download(local_file).execute_query()
    #file = ctx.web.get_file_by_server_relative_url(file_url).download(local_file).execute_query()
print("[Ok] file has been downloaded into: {0}".format(download_path))