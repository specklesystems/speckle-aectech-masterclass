

export const userInfoQuery = `
  query {
    user {
      name
      id
      avatar
      email
    },
    serverInfo {
      name
      company
    }
  }`

export const streamCommitsQuery = `
  query($id: String!, $limit: Int, $cursor: String) {
    stream(id: $id){
      name
      updatedAt
      id
      commits(limit: $limit, cursor: $cursor) {
        totalCount
        cursor
        items{
          id
          message
          branchName
          sourceApplication
          referencedObject
          authorName
          createdAt
        }
      }
    }
  }`

export const streamSearchQuery = `
  query($searchText: String!) {
    streams(query: $searchText) {
      totalCount
      cursor
      items {
        id
        name
        updatedAt
      }
    }
  }`

export const streamObjectQuery = `query($streamId: String!, $objectId: String!) {
    stream(id: $streamId){
        object(id: $objectId){
            totalChildrenCount
            id
            speckleType
            data
        }
    }
}`

export const latestStreamsQuery = `query {
    streams(limit: 10){
        cursor
        totalCount
        items {
            id
            name
            description
            createdAt
            updatedAt
        }
    }
}`