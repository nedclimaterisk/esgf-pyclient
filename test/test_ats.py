"""
Test Attribute Service API.

"""

from pyesgf.security.ats import AttributeService

CEDA_ATS = 'https://esgf-index1.ceda.ac.uk/esgf-idp/saml/soap/secure/attributeService.htm'

def test_ceda_ats():
    service = AttributeService(CEDA_ATS)
    openid = 'https://ceda.ac.uk/openid/Stephen.Pascoe'
    resp = service.send_request(openid, ['urn:esg:first:name', 'urn:esg:last:name'])

    assert resp.get_subject() == openid
    
    attrs = resp.get_attributes()
    assert attrs['urn:esg:first:name'] == 'Stephen'
    assert attrs['urn:esg:last:name'] == 'Pascoe'
    
def test_unkown_principal():
    service = AttributeService(CEDA_ATS)
    openid = 'https://example.com/unknown'

    resp = service.send_request(openid, [])

    assert resp.get_status() == 'urn:oasis:names:tc:SAML:2.0:status:UnknownPrincipal'

def test_multi_attribute():
    service = AttributeService(CEDA_ATS)

    openid = 'https://ceda.ac.uk/openid/Stephen.Pascoe'
    resp = service.send_request(openid, ['CMIP5 Research'])

    attrs = resp.get_attributes()
    assert list(sorted(attrs['CMIP5 Research'])) == ['default', 'user']
