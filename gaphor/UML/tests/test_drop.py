from gaphor import UML
from gaphor.diagram.drop import drop
from gaphor.UML.classes import PackageItem
from gaphor.UML.interactions import MessageItem
from gaphor.UML.interactions.interactionsconnect import connect_lifelines
from gaphor.UML.recipes import (
    create_association,
    create_extension,
    create_generalization,
)


def test_drop_class(diagram, element_factory):
    klass = element_factory.create(UML.Class)

    drop(klass, diagram, 0, 0)

    assert klass.presentation
    assert klass.presentation[0] in diagram.ownedPresentation


def test_drop_dependency(diagram, element_factory):
    client = element_factory.create(UML.Class)
    supplier = element_factory.create(UML.Class)
    dependency = element_factory.create(UML.Dependency)
    dependency.client = client
    dependency.supplier = supplier

    drop(client, diagram, 0, 0)
    drop(supplier, diagram, 0, 0)
    item = drop(dependency, diagram, 0, 0)

    assert (
        diagram.connections.get_connection(item.head).connected
        is supplier.presentation[0]
    )
    assert (
        diagram.connections.get_connection(item.tail).connected
        is client.presentation[0]
    )


def test_drop_association(diagram, element_factory):
    a = element_factory.create(UML.Class)
    b = element_factory.create(UML.Class)
    association = create_association(a, b)

    drop(a, diagram, 0, 0)
    drop(b, diagram, 0, 0)
    item = drop(association, diagram, 0, 0)

    assert item
    assert diagram.connections.get_connection(item.head).connected is a.presentation[0]
    assert diagram.connections.get_connection(item.tail).connected is b.presentation[0]


def test_drop_generalization(diagram, element_factory):
    a = element_factory.create(UML.Class)
    b = element_factory.create(UML.Class)
    generalization = create_generalization(a, b)

    drop(a, diagram, 0, 0)
    drop(b, diagram, 0, 0)
    item = drop(generalization, diagram, 0, 0)

    assert item
    assert diagram.connections.get_connection(item.head).connected is b.presentation[0]
    assert diagram.connections.get_connection(item.tail).connected is a.presentation[0]


def test_drop_extension(diagram, element_factory):
    metaclass = element_factory.create(UML.Class)
    stereotype = element_factory.create(UML.Stereotype)
    extension = create_extension(metaclass, stereotype)

    drop(metaclass, diagram, 0, 0)
    drop(stereotype, diagram, 0, 0)
    item = drop(extension, diagram, 0, 0)

    assert item
    assert (
        diagram.connections.get_connection(item.head).connected
        is metaclass.presentation[0]
    )
    assert (
        diagram.connections.get_connection(item.tail).connected
        is stereotype.presentation[0]
    )


def test_drop_message(diagram, element_factory):
    a = element_factory.create(UML.Lifeline)
    b = element_factory.create(UML.Lifeline)

    a_item = drop(a, diagram, 0, 0)
    b_item = drop(b, diagram, 0, 0)
    msg_item = diagram.create(MessageItem)
    connect_lifelines(msg_item, a_item, b_item)
    message = msg_item.subject

    item = drop(message, diagram, 0, 0)

    assert item
    assert diagram.connections.get_connection(item.head).connected is a.presentation[0]
    assert diagram.connections.get_connection(item.tail).connected is b.presentation[0]


def test_drop_message_send_connected(diagram, element_factory):
    a = element_factory.create(UML.Lifeline)

    a_item = drop(a, diagram, 0, 0)
    msg_item = diagram.create(MessageItem)
    connect_lifelines(msg_item, send=a_item, received=None)
    message = msg_item.subject

    item = drop(message, diagram, 0, 0)

    assert item
    assert diagram.connections.get_connection(item.head).connected is a.presentation[0]
    assert not diagram.connections.get_connection(item.tail)


def test_drop_message_received_connected(diagram, element_factory):
    b = element_factory.create(UML.Lifeline)

    b_item = drop(b, diagram, 0, 0)
    msg_item = diagram.create(MessageItem)
    connect_lifelines(msg_item, send=None, received=b_item)
    message = msg_item.subject

    item = drop(message, diagram, 0, 0)

    assert item
    assert not diagram.connections.get_connection(item.head)
    assert diagram.connections.get_connection(item.tail).connected is b.presentation[0]


def test_drop_pin(diagram, element_factory):
    action = element_factory.create(UML.Action)
    input_pin = element_factory.create(UML.InputPin)
    input_pin.opaqueAction = action
    output_pin = element_factory.create(UML.OutputPin)
    output_pin.opaqueAction = action

    drop(action, diagram, 0, 0)
    input_item = drop(input_pin, diagram, 0, 0)

    assert input_item
    assert input_item.subject is input_pin
    assert input_item.parent.subject is action

    ouput_item = drop(output_pin, diagram, 0, 0)

    assert ouput_item
    assert ouput_item.subject is output_pin
    assert ouput_item.parent.subject is action


def test_drop_element_on_presentation(diagram, element_factory):
    package_item = diagram.create(
        PackageItem, subject=element_factory.create(UML.Package)
    )
    cls = element_factory.create(UML.Class)

    drop(cls, package_item, 0, 0)
    class_item = cls.presentation[0]

    assert class_item.parent is package_item


def test_drop_element_on_presentation_that_cannot_be_owned(diagram, element_factory):
    package_item = diagram.create(
        PackageItem, subject=element_factory.create(UML.Package)
    )
    action = element_factory.create(UML.Action)

    drop(action, package_item, 0, 0)
    class_item = action.presentation[0]

    assert class_item.parent is None
