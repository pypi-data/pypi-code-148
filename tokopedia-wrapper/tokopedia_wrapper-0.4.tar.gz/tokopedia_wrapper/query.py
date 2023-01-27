PDPGetLayout = """
fragment ProductVariant on pdpDataProductVariant {
  errorCode
  parentID
  defaultChild
  sizeChart
  totalStockFmt
  variants {
    productVariantID
    variantID
    name
    identifier
    option {
      picture {
        urlOriginal: url
        urlThumbnail: url100
        __typename
      }
      productVariantOptionID
      variantUnitValueID
      value
      hex
      stock
      __typename
    }
    __typename
  }
  children {
    productID
    price
    priceFmt
    optionID
    optionName
    productName
    productURL
    picture {
      urlOriginal: url
      urlThumbnail: url100
      __typename
    }
    stock {
      stock
      isBuyable
      stockWordingHTML
      minimumOrder
      maximumOrder
      __typename
    }
    isCOD
    isWishlist
    campaignInfo {
      campaignID
      campaignType
      campaignTypeName
      campaignIdentifier
      background
      discountPercentage
      originalPrice
      discountPrice
      stock
      stockSoldPercentage
      startDate
      endDate
      endDateUnix
      appLinks
      isAppsOnly
      isActive
      hideGimmick
      isCheckImei
      minOrder
      __typename
    }
    thematicCampaign {
      additionalInfo
      background
      campaignName
      icon
      __typename
    }
    __typename
  }
  __typename
}

fragment ProductMedia on pdpDataProductMedia {
  media {
    type
    urlOriginal: URLOriginal
    urlThumbnail: URLThumbnail
    urlMaxRes: URLMaxRes
    videoUrl: videoURLAndroid
    prefix
    suffix
    description
    variantOptionID
    __typename
  }
  videos {
    source
    url
    __typename
  }
  __typename
}

fragment ProductHighlight on pdpDataProductContent {
  name
  price {
    value
    currency
    __typename
  }
  campaign {
    campaignID
    campaignType
    campaignTypeName
    campaignIdentifier
    background
    percentageAmount
    originalPrice
    discountedPrice
    originalStock
    stock
    stockSoldPercentage
    threshold
    startDate
    endDate
    endDateUnix
    appLinks
    isAppsOnly
    isActive
    hideGimmick
    __typename
  }
  thematicCampaign {
    additionalInfo
    background
    campaignName
    icon
    __typename
  }
  stock {
    useStock
    value
    stockWording
    __typename
  }
  variant {
    isVariant
    parentID
    __typename
  }
  wholesale {
    minQty
    price {
      value
      currency
      __typename
    }
    __typename
  }
  isCashback {
    percentage
    __typename
  }
  isTradeIn
  isOS
  isPowerMerchant
  isWishlist
  isCOD
  isFreeOngkir {
    isActive
    __typename
  }
  preorder {
    duration
    timeUnit
    isActive
    preorderInDays
    __typename
  }
  __typename
}

fragment ProductCustomInfo on pdpDataCustomInfo {
  icon
  title
  isApplink
  applink
  separator
  description
  __typename
}

fragment ProductInfo on pdpDataProductInfo {
  row
  content {
    title
    subtitle
    applink
    __typename
  }
  __typename
}

fragment ProductDetail on pdpDataProductDetail {
  content {
    title
    subtitle
    applink
    showAtFront
    isAnnotation
    __typename
  }
  __typename
}

fragment ProductDataInfo on pdpDataInfo {
  icon
  title
  isApplink
  applink
  content {
    icon
    text
    __typename
  }
  __typename
}

fragment ProductSocial on pdpDataSocialProof {
  row
  content {
    icon
    title
    subtitle
    applink
    type
    rating
    __typename
  }
  __typename
}

query PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String) {
  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam) {
    requestID
    name
    pdpSession
    basicInfo {
      alias
      createdAt
      isQA
      id: productID
      shopID
      shopName
      minOrder
      maxOrder
      weight
      weightUnit
      condition
      status
      url
      needPrescription
      catalogID
      isLeasing
      isBlacklisted
      menu {
        id
        name
        url
        __typename
      }
      category {
        id
        name
        title
        breadcrumbURL
        isAdult
        isKyc
        minAge
        detail {
          id
          name
          breadcrumbURL
          isAdult
          __typename
        }
        __typename
      }
      txStats {
        transactionSuccess
        transactionReject
        countSold
        paymentVerified
        itemSoldFmt
        __typename
      }
      stats {
        countView
        countReview
        countTalk
        rating
        __typename
      }
      __typename
    }
    components {
      name
      type
      position
      data {
        ...ProductMedia
        ...ProductHighlight
        ...ProductInfo
        ...ProductDetail
        ...ProductSocial
        ...ProductDataInfo
        ...ProductCustomInfo
        ...ProductVariant
        __typename
      }
      __typename
    }
    __typename
  }
}
"""