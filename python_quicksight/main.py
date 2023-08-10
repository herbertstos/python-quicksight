import boto3

from utils.constants import Constants


def get_session_boto3(**kwargs):
    session = boto3.Session(**kwargs)
    return session


def get_account_id(session):
    sts = session.client('sts')
    aws_account_id = sts.get_caller_identity()['Account']
    return aws_account_id


def get_client_qs(session):
    client = session.client('quicksight')
    return client


def _list_data_sets(profile_name='default', object_callback=None, max_results=50, **kwargs):
    """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_data_sets.html
        https://docs.aws.amazon.com/quicksight/latest/APIReference/API_ListDataSets.html
        :type object_callback: str: possible values: None, datasets
        :rtype: dict
    """
    is_first = True
    session = get_session_boto3(profile_name=profile_name)
    aws_account_id = get_account_id(session)
    client = get_client_qs(session)
    results = []

    response = client.list_data_sets(AwsAccountId=aws_account_id, MaxResults=max_results, **kwargs)
    results.append(response)

    while 'NextToken' in response:
        response = client.list_data_sets(AwsAccountId=aws_account_id,
                                         NextToken=response['NextToken'],
                                         MaxResults=max_results,
                                         **kwargs)
        results.append(response)

    if object_callback is None:
        return results
    if object_callback == Constants.DATASETS:
        _summaries = [_list['DataSetSummaries'] for _list in results]
        data_set_summaries = sum(_summaries, [])
        return data_set_summaries


if __name__ == '__main__':
    result = _list_data_sets(profile_name='wake', object_callback='datasets', max_results=50)
    # result = _list_data_sets(profile_name='wake', max_results=5)
    r = [[d['Name'], d['DataSetId']] for d in result]
    print(r)
