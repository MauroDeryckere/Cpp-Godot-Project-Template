#include "godot/MyNode.hpp"
#include "engine/Time.hpp"

#include <godot_cpp/core/class_db.hpp>
#include <godot_cpp/variant/utility_functions.hpp>

using namespace godot;

void MyNode::_ready()
{
    UtilityFunctions::print("MyNode ready with speed: ", m_Speed);
}

void MyNode::_process(double delta)
{
    engine::Time::Update(delta);

    m_TimeElapsed += delta * m_Speed;

    if (m_TimeElapsed >= 1.0)
    {
        m_TimeElapsed -= 1.0;
        emit_signal("tick");
    }
}

void MyNode::set_speed(double speed)
{
    m_Speed = speed;
}

double MyNode::get_speed() const
{
    return m_Speed;
}

void MyNode::_bind_methods()
{
    // Property: speed (visible in the Godot inspector)
    ClassDB::bind_method(D_METHOD("set_speed", "speed"), &MyNode::set_speed);
    ClassDB::bind_method(D_METHOD("get_speed"), &MyNode::get_speed);
    ADD_PROPERTY(PropertyInfo(Variant::FLOAT, "speed"), "set_speed", "get_speed");

    // Signal: tick (emitted once per second, scaled by speed)
    ADD_SIGNAL(MethodInfo("tick"));
}
