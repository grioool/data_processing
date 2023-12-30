### Data Processing in R and Python 2023Z
### Homework Assignment no. 2
###
### IMPORTANT
### This file should contain only solutions to tasks in the form of a functions
### definitions and comments to the code.
###
#
# Include imports here
import pandas as pd


# -----------------------------------------------------------------------------#
# Task 1
# -----------------------------------------------------------------------------#

def solution_1(Posts, Users):
    merged_df = pd.merge(Posts[['OwnerUserId']], Users[['Id', 'Location']], left_on='OwnerUserId', right_on='Id')
    location_counts = merged_df[merged_df['Location'] != ''].groupby('Location').size().reset_index(name='Count')

    best_locations = location_counts.sort_values(by='Count', ascending=False).head(10)
    best_locations.reset_index(drop=True, inplace=True)

    return best_locations


# -----------------------------------------------------------------------------#
# Task 2
# -----------------------------------------------------------------------------#


def solution_2(Posts, PostLinks):
    num_links_per_post = PostLinks.groupby('RelatedPostId').size().reset_index(name='NumLinks')
    related_posts = pd.merge(num_links_per_post, Posts[['Id', 'Title', 'PostTypeId']], left_on='RelatedPostId',
                             right_on='Id')

    related_posts = related_posts[related_posts['PostTypeId'] == 1]
    related_posts = related_posts.sort_values(by=['NumLinks', 'Id'], ascending=[False, True])
    related_posts = related_posts[['Title', 'NumLinks']]
    related_posts.reset_index(drop=True, inplace=True)

    return related_posts


# -----------------------------------------------------------------------------#
# Task 3
# -----------------------------------------------------------------------------#

def solution_3(Posts, Users, Comments):
    comments_total_score = Comments.groupby('PostId')['Score'].sum().reset_index(name='CommentsTotalScore')

    question_posts = Posts[Posts['PostTypeId'] == 1]
    merged_data = pd.merge(question_posts, comments_total_score, left_on='Id', right_on='PostId')

    highest_comment_scores = merged_data[['OwnerUserId', 'Title', 'CommentCount', 'ViewCount', 'CommentsTotalScore']]
    highest_comment_scores = pd.merge(highest_comment_scores, Users[['Id', 'DisplayName', 'Reputation', 'Location']],
                                      left_on='OwnerUserId', right_on='Id')

    highest_comment_scores = highest_comment_scores.sort_values(by='CommentsTotalScore', ascending=False).head(10)
    highest_comment_scores = highest_comment_scores[
        ['Title', 'CommentCount', 'ViewCount', 'CommentsTotalScore', 'DisplayName',
         'Reputation', 'Location']]
    highest_comment_scores.reset_index(drop=True, inplace=True)

    return highest_comment_scores


# -----------------------------------------------------------------------------#
# Task 4
# -----------------------------------------------------------------------------#

def solution_4(Posts, Users):
    answers_count = Posts[Posts['PostTypeId'] == 2].groupby('OwnerUserId').size().reset_index(name='AnswersNumber')
    questions_count = Posts[Posts['PostTypeId'] == 1].groupby('OwnerUserId').size().reset_index(name='QuestionsNumber')

    merged_counts = pd.merge(answers_count, questions_count, on='OwnerUserId')
    filtered_users = merged_counts[merged_counts['AnswersNumber'] > merged_counts['QuestionsNumber']]

    best_users = pd.merge(filtered_users,
                          Users[['Id', 'DisplayName', 'Location', 'Reputation', 'UpVotes', 'DownVotes']],
                          left_on='OwnerUserId', right_on='Id').sort_values(by='AnswersNumber', ascending=False).head(5)
    best_users = best_users[['DisplayName', 'QuestionsNumber', 'AnswersNumber', 'Location', 'Reputation',
                             'UpVotes', 'DownVotes']]
    best_users.reset_index(drop=True, inplace=True)

    return best_users


# -----------------------------------------------------------------------------#
# Task 5
# -----------------------------------------------------------------------------#

def solution_5(Posts):
    best_answers = Posts[Posts['PostTypeId'] == 2].groupby('ParentId')['Score'].max().reset_index(name='MaxScore')
    questions = Posts[Posts['PostTypeId'] == 1][['Id', 'Title', 'AcceptedAnswerId']]

    merged_best_questions = pd.merge(best_answers, questions, left_on='ParentId', right_on='Id')
    accepted_answers = Posts[['Id', 'Score']].rename(columns={'Score': 'AcceptedScore'})

    questions_answers = pd.merge(merged_best_questions, accepted_answers, left_on='AcceptedAnswerId', right_on='Id')
    questions_answers['Difference'] = questions_answers['MaxScore'] - questions_answers['AcceptedScore']

    biggest_differences = questions_answers[questions_answers['Difference'] > 50].sort_values(
        by=['Difference', 'Id_x'],
        ascending=[False, True])
    biggest_differences = (biggest_differences[['Id_x', 'Title', 'MaxScore', 'AcceptedScore', 'Difference']]
                           .rename(columns={'Id_x': 'Id'}))
    biggest_differences.reset_index(drop=True, inplace=True)

    return biggest_differences
